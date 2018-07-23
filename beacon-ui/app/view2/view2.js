'use strict';

angular.module('myApp.view2', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/view2', {
    templateUrl: 'view2/view2.html',
    controller: 'View2Ctrl'
  });
}])

.controller('View2Ctrl', ['$scope', '$http', function($scope, $http) {
  $scope.message = "";
  $scope.search = {type: 'disease', query: ''};
  $scope.assembly = {selected: 'GRCh38'};
  $scope.url = '';
  $scope.cookieLoggedIn = false;

  $scope.baseUrl = 'http://beacon-search-beacon.rahtiapp.fi//api?';
  $scope.urlDisease = 'disease=';
  $scope.urlGene = 'gene=';
  $scope.urlAssembly = '&assembly=';

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
      $scope.url = 'http://beacon-aggregator-beacon.rahtiapp.fi//q?ref='+$scope.assembly.selected+'&chrom='+qs[0]+'&pos='+qs[2]+'&allele='+qs[5];
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
      url: 'http://beacon-aggregator-beacon.rahtiapp.fi//q?ref='+assembly+'&chrom='+chr+'&pos='+pos+'&allele='+alt
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
