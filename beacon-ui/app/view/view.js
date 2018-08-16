'use strict';

angular.module('beaconApp.view', ['ngRoute', 'ngMaterial', 'ngMessages', 'ui.bootstrap'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/view', {
    templateUrl: 'view/view.html',
    controller: 'ViewCtrl'
  });
}])

.controller('ViewCtrl', ['$scope', '$http', function($scope, $http) {
  var that = this;
  that.searchText = "";
  that.selectedItem = '';
  that.message = "";
  that.searchClick = false;
  $scope.search = {type: 'disease', query: ''};
  $scope.assembly = {selected: 'GRCh38'};
  $scope.url = '';
  $scope.cookieLoggedIn = false;
  that.triggerCredentials = false;
  that.userid = 'abc123@elixir-europe.org'

  $scope.baseUrl = 'https://beacon-search-beacon.rahtiapp.fi';
  $scope.autocompleteUrl = $scope.baseUrl + '/autocomplete?';
  $scope.urlDisease = 'disease=';
  $scope.urlGene = 'gene=';
  $scope.urlAssembly = '&assembly=';

  $scope.aggregatorUrl = 'https://beacon-aggregator-beacon.rahtiapp.fi/q?';

  $scope.selectedItem = null;

  that.regexp = /^([XY0-9]+) \: (\d+) ([ATCGN]+) \> ([ATCGN]+)$/i;



  function makeUrl(searchtype, query) {
    if (searchtype == 'disease') {
      return $scope.baseUrl + $scope.urlDisease + query
    } else if (searchtype == 'gene') {
      return $scope.baseUrl + $scope.urlGene + query
    } else if (searchtype == 'variant') {
      return $scope.aggregatorUrl + query
    } else {
      return 'Invalid Searchtype'
    }
  }

  that.querySearch = function(query){
    if (query && that.searchText.length >= 2) {
      return $http.get($scope.autocompleteUrl, {params: {q: query}})
      .then(function(response){
        return response.data;
      })
    } else {
      return {};
    }
  }

  // Pagination settings
  $scope.maxSize = 5;
  $scope.totalItems = 640;
  $scope.currentPage = 1;
  $scope.viewby = 20;
  $scope.itemsPerPage = $scope.viewby;
  

  $scope.setPage = function (pageNo) {
    $scope.currentPage = pageNo;
  };

  $scope.pageChanged = function() {
    $log.log('Page changed to: ' + $scope.currentPage);
  };

  $scope.setItemsPerPage = function(num) {
    $scope.itemsPerPage = num;
    $scope.currentPage = 1; //reset to first page
  }




  $scope.generatePagination = function(pagination_data) {
    // Generate range for pages
    var array = [];
    for (var i = 1; i <= pagination_data['totalPages']; i++) {
      array.push(i);
    }
    return array;
  }

  $scope.selectPage = function(page, resultsPerPage, action=false, totalPages=false) {
    if (action == 'prev' && page > 1) {page--;}
    if (action == 'next' && page < totalPages) {page++;}

    $scope.url = $scope.baseUrl + '/api?' + 'type=' + that.selectedItem.type + 
                 '&query=' + that.searchText + ',' + $scope.assembly.selected + 
                 '&page=' + page + '&resultsPerPage=' + resultsPerPage;

    $http({
      method: 'GET',
      url: $scope.url
    }).then(function successCallback(response) {
        console.log(response);
        that.message = response;
      }, function errorCallback(response) {
      });
  }

  // Simple GET request example:
  $scope.submit = function() {
    that.message = 'loading';
    that.searchClick = true;
    if (that.regexp.test(that.searchText)) {
      that.selectedItem = {type: 'variant', name: that.searchText}
    }
    if (that.selectedItem && that.selectedItem.type == 'disease') {
      that.triggerCredentials = false;
      $scope.url = $scope.baseUrl + '/api?' + 'type=' + that.selectedItem.type + '&query=' + that.searchText;
      console.log($scope.url);
    } else if (that.selectedItem && that.selectedItem.type == 'gene') {
      that.triggerCredentials = false;
      $scope.url = $scope.baseUrl + '/api?' + 'type=' + that.selectedItem.type + '&query=' + that.searchText + ',' + $scope.assembly.selected;
      console.log($scope.url);
    } else if (that.selectedItem && that.selectedItem.type == 'variant') {
      that.triggerCredentials = true;
      var params = that.searchText.match(that.regexp)
      $scope.url = $scope.aggregatorUrl + 'assemblyId=' +
                   $scope.assembly.selected +
                   '&referenceName=' + params[1] + '&start=' + params[2]+
                   '&referenceBases=' + params[3] + '&alternateBases=' + params[4];
      console.log($scope.url);
    } else {
      console.log('search type unselected');
    }

    $http({
      method: 'GET',
      url: $scope.url,
      withCredentials: that.triggerCredentials
    }).then(function successCallback(response) {
        console.log(response);
        that.message = response;
      }, function errorCallback(response) {
      });
  }

  $scope.searchExample = function(searchtype) {
    if (searchtype == 'disease') {
      that.searchText = 'Alzheimer';
      document.querySelector('#autoCompleteId').focus();
    } else if (searchtype == 'gene') {
      that.searchText = 'APOE';
      document.querySelector('#autoCompleteId').focus();
    } else if (searchtype == 'variant') {
      that.searchText = '19 : 44907807 G > A';
      document.querySelector('#autoCompleteId').focus();
    } else {
      that.searchText = 'Unknown';
    }
  }

  $scope.goToGene = function(gene) {
    that.message = 'loading';
    that.selectedItem = {'type': 'gene', 'name': gene};
    that.searchText = gene;
    $scope.url = $scope.baseUrl + '/api?' + 'type=' + that.selectedItem.type + '&query=' + that.searchText + ',' + $scope.assembly.selected;
    console.log($scope.url);

    $http({
      method: 'GET',
      url: $scope.url
    }).then(function successCallback(response) {
        console.log(response);
        that.message = response;
      }, function errorCallback(response) {
        console.log("failure");
      });
  }

  $scope.findDatasets = function(chr, pos, ref, alt, assembly) {
    that.message = 'loading';
    that.selectedItem = {type: 'variant', name: chr + ' : ' + pos + ' ' + ref + ' > ' + alt};

    $http({
      method: 'GET',
      withCredentials: true,
      url: $scope.url = $scope.aggregatorUrl + 'assemblyId='+ assembly +
                        '&referenceName='+ chr + '&start=' + pos +
                        '&referenceBases=' + ref + '&alternateBases=' + alt
    }).then(function successCallback(response) {
        console.log(response);
        that.message = response;
      }, function errorCallback(response) {
        console.log("failure");
        $scope.err = 'Input is in incorrect format, or the API is offline.'
      });
  }

	}]);
