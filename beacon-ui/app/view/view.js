'use strict';

angular.module('beaconApp.view', ['ngRoute', 'ngMaterial', 'ngMessages', 'ngCookies', 'ui.bootstrap', 'angular.filter'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/view', {
    templateUrl: 'view/view.html',
    controller: 'ViewCtrl'
  });
}])

.controller('ViewCtrl', ['$scope', '$http', '$cookies', function($scope, $http, $cookies) {
  var that = this;
  that.searchText = "";
  that.selectedItem = '';
  that.message = "";
  that.searchClick = false;

  that.triggerCredentials = false;

  $scope.search = {type: 'disease', query: ''};
  $scope.assembly = {selected: 'GRCh38'};
  $scope.url = '';
  $scope.baseUrl = '';
  $scope.aggregatorUrl = '';
  $scope.autocompleteUrl = '';
  $http.get('view/config.json').success(function (data){
		$scope.baseUrl = data.baseUrl;
    $scope.aggregatorUrl = data.aggregatorUrl;
    $scope.autocompleteUrl = $scope.baseUrl + '/autocomplete?';
	});

  // $scope.object = {alertType : true}
    // $scope.alertType = true;
  if($cookies.get('info') != null) {
    console.log('cookie was set');
    $scope.alertType = false;
  } else {
    console.log('cookie was not set');
    $scope.alertType = true;
  }
  $scope.acknowledge = function() {
      var when = new Date();
      var mm =when.getMonth() + 2;
      var y = when.getFullYear();
      $cookies.put("info", "acknowledged", {
        expires: new Date(y, mm),
        path: '/'
      });
      console.log('cookie was set');
      $scope.alertType = false;
  };

  that.regexp = /^(X|Y|MT|[1-9]|1[0-9]|2[0-2]) \: (\d+) ([ATCGN]+) \> ([ATCGN]+)$/i;

  $scope.checkLogin = function() {
    if($cookies.get('access_token')) {
      return true;
    } else {
      return false;
    }
  }

  $scope.checkBonaFide = function() {
    if($cookies.get('bona_fide_status')) {
      return true;
    } else {
      return false;
    }
  }

  $scope.classRow = "resultCard";
  $scope.changeCardClass = function(display){
      $scope.classRow = display;
   };

  that.querySearch = function(query){
    that.searchClick = false;
    if (query && that.searchText.length >= 2) {
      // return $http.get($scope.autocompleteUrl, {params: {q: query}})
      // .then(function(response){
      //   return response.data;
      // })
      return {};
    } else {
      return {};
    }
  }

  // Pagination settings
  $scope.maxSize = 5;
  $scope.currentPage = 1;
  $scope.viewby = 10;
  $scope.itemsPerPage = $scope.viewby;


  $scope.setPage = function (pageNo) {
    $scope.currentPage = pageNo;
  };

  $scope.pageChanged = function(page) {
    $scope.currentPage = page;
    select($scope.currentPage, $scope.itemsPerPage);
  };

  $scope.setItemsPerPage = function(num) {
    $scope.itemsPerPage = num;
    $scope.pageChanged($scope.currentPage);
  }

  function select (page, resultsPerPage) {
  if(that.selectedItem.type == 'disease'){
    $scope.url = $scope.baseUrl + '/api?' + 'type=' + that.selectedItem.type +
                 '&query=' + that.searchText +
                 '&page=' + page + '&resultsPerPage=' + resultsPerPage;

  } else {
    $scope.url = $scope.baseUrl + '/api?' + 'type=' + that.selectedItem.type +
                 '&query=' + that.searchText + ',' + $scope.assembly.selected +
                 '&page=' + page + '&resultsPerPage=' + resultsPerPage;
  }

    $http({
      method: 'GET',
      url: $scope.url
    }).then(function successCallback(response) {
        that.message = response;
      }, function errorCallback(response) {
      });
  }

  // Simple GET request example:
  $scope.submit = function() {
    that.message = 'loading';
    that.searchClick = true;
    $scope.itemsPerPage = 10;
    if (that.regexp.test(that.searchText)) {
      that.selectedItem = {type: 'variant', name: that.searchText}

    }
    // if (that.selectedItem && that.selectedItem.type == 'disease') {
    //   that.triggerCredentials = false;
    //   $scope.url = $scope.baseUrl + '/api?' + 'type=' + that.selectedItem.type + '&query=' + that.searchText;
    // } else if (that.selectedItem && that.selectedItem.type == 'gene') {
    //   that.triggerCredentials = false;
    //   $scope.url = $scope.baseUrl + '/api?' + 'type=' + that.selectedItem.type + '&query=' + that.searchText + ',' + $scope.assembly.selected;
    // } else
    if (that.selectedItem && that.selectedItem.type == 'variant') {
      that.triggerCredentials = true;
      var params = that.searchText.match(that.regexp)
      $scope.url = $scope.aggregatorUrl + 'assemblyId=' +
                   $scope.assembly.selected +
                   '&referenceName=' + params[1] + '&start=' + params[2] +
                   '&referenceBases=' + params[3] + '&alternateBases=' + params[4] +
                   '&includeDatasetResponses=HIT';
    } else {
      console.log('search type unselected');
    }

    $http({
      method: 'GET',
      url: $scope.url,
      withCredentials: that.triggerCredentials
    }).then(function successCallback(response) {
        that.message = response;
      }, function errorCallback(response) {
      });
  }

  $scope.searchExample = function(searchtype) {
    that.searchClick = false;
    // if (searchtype == 'disease') {
    //   that.searchText = 'Alzheimer';
    //   document.querySelector('#autoCompleteId').focus();
    // } else if (searchtype == 'gene') {
    //   that.searchText = 'APOE';
    //   document.querySelector('#autoCompleteId').focus();
    // } else
    if (searchtype == 'variant') {
      // Maybe add examples for other chromosomes later when we have more datasets
      var variants = ['MT : 10 T > C', 'MT : 7600 G > A', 'MT : 195 TTACTAAAGT > CCACTAAAGT', 'MT : 14037 A > G']
      // Select example variant from list at random
      that.searchText = variants[Math.floor(Math.random()*variants.length)];
      document.querySelector('#autoCompleteId').focus();
    } else {
      that.searchText = 'Unknown';
    }
  }

  $scope.goToGene = function(gene) {
    that.message = 'loading';
    that.searchClick = false;
    that.selectedItem = {'type': 'gene', 'name': gene};
    that.searchText = gene;
    $scope.url = $scope.baseUrl + '/api?' + 'type=' + that.selectedItem.type + '&query=' + that.searchText + ',' + $scope.assembly.selected;

    $http({
      method: 'GET',
      url: $scope.url
    }).then(function successCallback(response) {
        that.message = response;
      }, function errorCallback(response) {
      });
  }

  $scope.findDatasets = function(chr, pos, ref, alt, assembly) {
    that.searchClick = false;
    that.message = 'loading';
    that.selectedItem = {type: 'variant', name: chr + ' : ' + pos + ' ' + ref + ' > ' + alt};

    $http({
      method: 'GET',
      withCredentials: true,
      url: $scope.url = $scope.aggregatorUrl + 'assemblyId='+ assembly +
                        '&referenceName='+ chr + '&start=' + pos +
                        '&referenceBases=' + ref + '&alternateBases=' + alt +
                        '&includeDatasetResponses=HIT'
    }).then(function successCallback(response) {
        that.message = response;
      }, function errorCallback(response) {
        $scope.err = 'API is offline.'
      });
  }

	}]);
