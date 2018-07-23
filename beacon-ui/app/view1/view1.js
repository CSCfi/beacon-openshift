'use strict';

angular.module('myApp.view1', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/view1', {
    templateUrl: 'view1/view1.html',
    controller: 'View1Ctrl'
  });
}])

.controller('View1Ctrl', ['$scope', '$http', function($scope, $http) {
  $scope.message = "Hello world!";
  $scope.search = {query: ''};
	$scope.url = 'http://86.50.169.120:9000/api?gene=';
	$scope.assembly = '&assembly=GRCh38';

  // Simple GET request example:
  $scope.submit = function() {
    $http({
      method: 'GET',
      url: $scope.url + $scope.search.query + $scope.assembly
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
      });
  }
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
