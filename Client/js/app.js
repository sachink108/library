'use strict';

// define the AngularJS application. Include the ngRoute and ngResource modules
//var app = angular.module('libApp', ['ngRoute', 'ngResource', 'ui.bootstrap', 'ngAnimate']);
var app = angular.module('libApp', ['ngRoute', 'ngResource', 'ngCookies', 'ui.bootstrap']);

app.config(['$routeProvider', function ($routeProvider) {

   $routeProvider
        .when('/login', {
            controller: 'LoginController',
            templateUrl: 'html/login.html',
            hideMenus: true
        })
 
        .when('/home', {
            controller: 'HomeController',
            templateUrl: 'html/home.html'
        })
        .when('/newuser', {
            controller: 'NewUserController',
            templateUrl: 'html/newuser.html'
        })
        .when('/', {
            controller : 'LoginController',
            templateUrl: 'html/login.html'
        })
        
        .otherwise({ redirectTo: '/login' });
}])
.run(['$rootScope', '$location', '$cookieStore', '$http',
    function ($rootScope, $location, $cookieStore, $http) {
        // keep user logged in after page refresh
        $rootScope.globals = $cookieStore.get('globals') || {};
        if ($rootScope.globals.currentUser) {
            console.log("GLobals current user");
            //$http.defaults.headers.common['Authorization'] = 'Basic ' + $rootScope.globals.currentUser.authdata; // jshint ignore:line
        }
 
        $rootScope.$on('$locationChangeStart', function (event, next, current) {
            console.log("Redirecting ... " + $location.path());
            // redirect to login page if not logged in
            if ($location.path() == '/newuser') {
                $location.path('/newuser');
            } 
            else if ($location.path() !== '/login' && !$rootScope.globals.currentUser) {
            // redirect to login page if not logged in
               $location.path('/login');
            }
        });
    }]);
