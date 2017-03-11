'use strict';

app.controller('HomeController', ['$rootScope','$scope', '$cookieStore', function ($scope, $rootScope, $cookieStore) {
    console.log("Home controller initialized");
    var globals = $cookieStore.get('globals');
    console.log(globals);
    $scope.username = globals.currentUser.username;
    $scope.toggle = true;
    $scope.showHide = "Show Categories";
    
    $scope.toggleCat = function() {
        console.log("CLicked");
        $("#wrapper").toggleClass("toggled");
        $scope.showHide = $scope.showHide === "Show Categories" ? "Hide Categories" : "Show Categories";
    };
}]);