'use strict';

app.controller('LoginController', ['$scope', '$http', '$rootScope', '$location', 'AuthenticationService',
               function($scope, $http, $rootScope, $location, AuthenticationService) {
    AuthenticationService.ClearCredentials(); // reset login status
    
    $scope.login = function() {
        $scope.dataLoading = true;
        console.log("Sending to authenticate");
        AuthenticationService.Login($scope.username, $scope.password, function(response) {
            if(response.status === 'success') {
                console.log("inCallback");
                AuthenticationService.SetCredentials($scope.username, $scope.password);
                $location.path('/home');
            } else {
                $scope.error = "Invalid Username or Password";
                $scope.dataLoading = false;
            }
        });
        //$location.path('/home');
    };
}]);

