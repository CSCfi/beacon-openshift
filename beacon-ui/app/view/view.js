'use strict';

angular.module('beaconApp.view', ['ngRoute', 'ngMaterial', 'ngMessages'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/view', {
    templateUrl: 'view/view.html',
    controller: 'ViewCtrl'
  });
}])

.controller('ViewCtrl', ['$scope', '$http', function($scope, $http) {
  var that = this;
  that.searchText = "";
  that.selectedItem = "";
  that.message = "";
  $scope.search = {type: 'disease', query: ''};
  $scope.assembly = {selected: ''};
  $scope.url = '';
  $scope.cookieLoggedIn = false;

  $scope.baseUrl = 'https://beacon-search-beacon.rahtiapp.fi';
  $scope.autocompleteUrl = $scope.baseUrl + '/autocomplete?';
  $scope.urlDisease = 'disease=';
  $scope.urlGene = 'gene=';
  $scope.urlAssembly = '&assembly=';

  $scope.aggregatorUrl = 'https://beacon-aggregator-beacon.rahtiapp.fi/q?';

  $scope.selectedItem = null;


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
    // if (query && query.length >= 2) {
      return $http.get($scope.autocompleteUrl, {params: {q: query}})
      // return $http.get(makeUrl($scope.search.type, query))
      .then(function(response){
        return response.data;
      })
    // }
  }



  // Simple GET request example:
  $scope.submit = function() {
    if ($scope.search.type == 'disease') {
      console.log('search type: ' + $scope.search.type);
      $scope.url = $scope.baseUrl + '/api?' + 'type=' + that.selectedItem.type + '&query=' + that.searchText;
      console.log($scope.url);
    } else if ($scope.search.type == 'gene') {
      console.log('search type: ' + $scope.search.type);
      $scope.url = $scope.baseUrl + $scope.urlGene + $scope.search.query + $scope.urlAssembly + $scope.assembly.selected;
      console.log($scope.url);
    } else if ($scope.search.type == 'variant') {
      console.log('search type: ' + $scope.search.type);
      var qs = $scope.search.query.split(" ");
      $scope.url = 'https://beacon-aggregator-beacon.rahtiapp.fi/q?assemblyId='+$scope.assembly.selected+'&referenceName='+qs[0]+'&start='+qs[2]+'&referenceBases='+qs[3]+'&alternateBases='+qs[5];
      console.log($scope.url);
      $scope.message = 'q';
    } else {
      console.log('search type unselected');
    }

    $http({
      method: 'GET',
      url: $scope.url
      // params: {}
    }).then(function successCallback(response) {
        console.log(response);
        that.message = response;
        //$scope.disease = response.data[0].disease;
        // this callback will be called asynchronously
        // when the response is available
      }, function errorCallback(response) {
        console.log("failure");
        $scope.err = 'Input is in incorrect format, or the API is offline.'
        // called asynchronously if an error occurs
        // or server returns response with an error status.
      });
  }

  $scope.searchExample = function(searchtype) {
    if (searchtype == 'disease') {
      this.searchText = 'Alzheimer';
    } else if (searchtype == 'gene') {
      $scope.searchText = 'APOE';
    } else if (searchtype == 'variant') {
      $scope.searchText = '19 : 44907807 G > A';
    } else {
      $scope.searchText = 'Unknown';
    }
  }

  $scope.goToGene = function(gene) {
    $scope.search.type = 'gene';
    $scope.search.query = gene;
    $scope.url = $scope.baseUrl + $scope.urlGene + $scope.search.query + $scope.urlAssembly + $scope.assembly.selected;

    $http({
      method: 'GET',
      url: $scope.url
    }).then(function successCallback(response) {
        console.log(response);
        $scope.message = response;
        //$scope.disease = response.data[0].disease;
        // this callback will be called asynchronously
        // when the response is available
      }, function errorCallback(response) {
        console.log("failure");
        // called asynchronously if an error occurs
        // or server returns response with an error status.
      });
  }

  $scope.findDatasets = function(chr, pos, ref, alt, assembly) {
    $scope.message = 'q';
    $scope.search.type = 'variant';
    $scope.assembly.selected = assembly;
    $scope.search.query = chr + ' : ' + pos + ' ' + ref + ' > ' + alt;

    $http({
      method: 'GET',
      url: $scope.url = 'https://beacon-aggregator-beacon.rahtiapp.fi/q?assemblyId='+$scope.assembly.selected+'&referenceName='+qs[0]+'&start='+qs[2]+'&referenceBases='+qs[3]+'&alternateBases='+qs[5]
    }).then(function successCallback(response) {
        console.log(response);
        $scope.message = response;
        //$scope.disease = response.data[0].disease;
        // this callback will be called asynchronously
        // when the response is available
      }, function errorCallback(response) {
        console.log("failure");
        $scope.err = 'Input is in incorrect format, or the API is offline.'
        // called asynchronously if an error occurs
        // or server returns response with an error status.
      });
  }

	}]);
