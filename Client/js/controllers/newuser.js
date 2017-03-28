'use strict';

app.controller('NewUserController', ['$scope', '$http', '$rootScope', '$location', function($scope, $http, $rootScope, $location) {
    $scope.name = '';
    $scope.pass = '';
    
    $scope.register = function() {
        console.log("Registering User");
        $http({method:'POST', 
               url:'http://localhost:9000/newuser/username=' +$scope.username+',password='+$scope.password, 
               timeout: 5000}
             )
             .success(function(data, status, headers, config) {
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

