'use strict';

angular.module('myApp.view', ['ngRoute', 'ngMaterial', 'ngMessages'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/view', {
    templateUrl: 'view/view.html',
    controller: 'ViewCtrl'
  });
}])

.controller('ViewCtrl', ['$scope', '$http', function($scope, $http) {
  $scope.message = "";
  $scope.search = {type: 'disease', query: ''};
  $scope.assembly = {selected: ''};
  $scope.url = '';
  $scope.cookieLoggedIn = false;

  $scope.baseUrl = 'https://beacon-search-beacon.rahtiapp.fi/api?';
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

  this.querySearch = function(query){
    return $http.get($scope.baseUrl, {params: {type: $scope.search.type, query: query}})
    // return $http.get(makeUrl($scope.search.type, query))
    .then(function(response){
      return response.data;
    })
  }



  // Simple GET request example:
  $scope.submit = function() {
    if ($scope.search.type == 'disease') {
      console.log('search type: ' + $scope.search.type);
      $scope.url = $scope.baseUrl + $scope.urlDisease + $scope.search.query;
      console.log($scope.url);
    } else if ($scope.search.type == 'gene') {
      console.log('search type: ' + $scope.search.type);
      $scope.url = $scope.baseUrl + $scope.urlGene + $scope.search.query + $scope.urlAssembly + $scope.assembly.selected;
      console.log($scope.url);
    } else if ($scope.search.type == 'variant') {
      console.log('search type: ' + $scope.search.type);
      var qs = $scope.search.query.split(" ");
      $scope.url = 'http://localhost:5000/q?ref='+$scope.assembly.selected+'&chrom='+qs[0]+'&pos='+qs[2]+'&allele='+qs[5];
      console.log($scope.url);
      $scope.message = 'q';
    } else {
      console.log('search type unselected');
    }

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
        $scope.err = 'Input is in incorrect format, or the API is offline.'
        // called asynchronously if an error occurs
        // or server returns response with an error status.
      });
  }

  $scope.searchExample = function(searchtype) {
    if (searchtype == 'disease') {
      $scope.search.query = 'Alzheimer';
    } else if (searchtype == 'gene') {
      $scope.search.query = 'APOE';
    } else if (searchtype == 'variant') {
      $scope.search.query = '19 : 44907807 G > A';
    } else {
      $scope.search.query = 'Unknown';
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
      url: 'http://localhost:5000/q?ref='+assembly+'&chrom='+chr+'&pos='+pos+'&allele='+alt
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
  /*
  $scope.urlGene = 'http://86.50.169.120:9000/api?gene=';
	$scope.assembly = '&assembly=GRCh38';  // preset for now

  // Simple GET request example:
  $scope.browseMutations = function() {
    $http({
      method: 'GET',
      url: $scope.urlGene + $scope.search.query + $scope.assembly
    }).then(function successCallback(response) {
        console.log(response);
        $scope.genemsg = response;
        // this callback will be called asynchronously
        // when the response is available
      }, function errorCallback(response) {
        console.log("failure");
        // called asynchronously if an error occurs
        // or server returns response with an error status.
      });
  }*/
  /*
	$http({
	  method: 'GET',
	  url: 'http://86.50.169.120:9000/d/' + $scope.search.query + '/more'
	}).then(function successCallback(response) {
	    console.log(response);
	    $scope.message = response;
	    $scope.disease = response.data[0].disease;
	    // this callback will be called asynchronously
	    // when the response is available
	  }, function errorCallback(response) {
	    console.log("failure");
	    // called asynchronously if an error occurs
	    // or server returns response with an error status.
	  });*/
	}]);
