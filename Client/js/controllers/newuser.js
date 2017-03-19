'use strict';

app.controller('NewUserController', ['$scope', '$http', '$rootScope', '$location', function($scope, $http, $rootScope, $location) {
    $scope.name = '';
    $scope.pass = '';
    
    $scope.register = function() {
        console.log("Registering User");
        $http({method:'POST', 
               url:'http://localhost:9000/newuser/name=' +$scope.username+',password='+$scope.password, 
               timeout: 5000}
             )
             success(function(data, status, headers, config) {
                if (data.status === "exists") {
                    $scope.warning = "User already Exists";
                    console.log($scope.warning);
                } else {
                    $scope.info = "User Added";
                    console.log($scope.info);
                    $location.path('/home');
                }
            }).error(function(data, status, headers, config) {
                $scope.error = "Unable to register user";
                console.log($scope.error);
                $scope.auth = "fail";
            });
        };
}]);

/*
'use strict';
 
angular.module('Authentication')
 
.controller('LoginController',
    ['$scope', '$rootScope', '$location', 'AuthenticationService',
    function ($scope, $rootScope, $location, AuthenticationService) {
        // reset login status
        AuthenticationService.ClearCredentials();
 
        $scope.login = function () {
            $scope.dataLoading = true;
            AuthenticationService.Login($scope.username, $scope.password, function(response) {
                if(response.success) {
                    AuthenticationService.SetCredentials($scope.username, $scope.password);
                    $location.path('/library');
                } else {
                    $scope.error = response.message;
                    $scope.dataLoading = false;
                }
            });
        };
    }]);

*/