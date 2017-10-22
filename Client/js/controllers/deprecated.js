// This function only to preview the image
    // to upload we are reading it again and POST'int it
    /* // This function seems simpler and use a Promise
    //http://stackoverflow.com/questions/32556664/getting-byte-array-through-input-type-file
    $scope.readURL = function(input) {
        var files = input.files;
        $scope.fileData = new Blob([files[0]]);
        // Pass getBuffer to promise.
        var promise = new Promise(getBuffer);
        // Wait for promise to be resolved, or log error.
        promise.then(function(data) {
            console.log(data);
            
            $http({method: 'POST', 
                   url: "http://localhost:9000/addbook/",
                   data: {
                            "author":"sachin kulkarni",
                            "title":"glutton for punishment 1000",
                            "image" : data,
                            "user" : $scope.username
                        },
                   timeout: 5000,
                   headers: {'Content-Type': 'application/x-www-form-urlencoded'} 
                   })
            .success(function(data) {
                console.log(data);
                if(data.status === 'OK') {
                    console.log("Uploaded content.");
                    $uibModalInstance.close();
                }
                else {
                    console.log("Could not upload content");
                }
            })
            .error(function(data) {
                console.log("ERRRRR!");
            });
            
            
        }).catch(function(err) {
            console.log('Error: ',err);
        });
    };
    
    function getBuffer(resolve) {
        var reader = new FileReader();
        reader.readAsArrayBuffer($scope.fileData);
        reader.onload = function() {
            var arrayBuffer = reader.result
            var bytes = new Uint8Array(arrayBuffer);
            resolve(bytes);
        }
    }
    */
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
$http({
            method: 'POST',
            url: 'http://localhost:9000/addbook',
            headers: {
                //'Content-Type': 'multipart/form-data'
            },
            data: {
                author: 'lee child',
                title: 'make me',
                upload: $scope.file
            },
            transformRequest: function (data, headersGetter) {
                var formData = new FormData();
                angular.forEach(data, function (value, key) {
                    formData.append(key, value);
                });

                var headers = headersGetter();
                delete headers['Content-Type'];

                return formData;
            }
        })
        .success(function (data) {

        })
        .error(function (data, status) {

        });
        /*
app.directive('file', function () {
    return {
        scope: {
            file: '='
        },
        link: function (scope, el, attrs) {
            el.bind('change', function (event) {
                var file = event.target.files[0];
                scope.file = file ? file : undefined;
                scope.$apply();
            });
        }
    };
});
*/

/*
        var title = $('#title').val();
        var author = $('#author').val();
        var reader = new FileReader();
        reader.readAsDataURL($scope.img_file);
        reader.onload = function(e) {
            console.log("POSTING " + title + " " + author + " " + $scope.img_file.name);            
            console.log(e.target.result);
            $http({method: 'POST', 
                   url: "http://localhost:9000/addbook/",
                   data: {
                            "author":"sachin kulkarni",
                            "title":"glutton for punishment 1000",
                            "data" : e.target.result,
                            "user" : $scope.username
                        },
                   timeout: 5000,
                   headers: {'Content-Type': 'application/x-www-form-urlencoded'} 
                   })
            .success(function(data) {
                console.log(data);
                if(data.status === 'OK') {
                    console.log("Uploaded content.");
                    $uibModalInstance.close();
                }
                else {
                    console.log("Could not upload content");
                }
            })
            .error(function(data) {
                console.log("ERRRRR!");
            });
        };
        */
        <!--<button type="submit" class="btn btn-primary">Submit</button>-->

        /*
app.controller('LoginController', ['$scope', '$http', '$rootScope', '$location', 'AuthenticationService',
               function($scope, $http, $rootScope, $location, AuthenticationService) {
    //AuthenticationService.ClearCredentials(); // reset login status
    $scope.signedIn = false;

    $scope.signInCallback = function(authResult) {
        console.log("in function signInCallback()");
            if (authResult['code']) {
                // Hide the sign-in button now that the user is authorized, for example:
                //$('#signinButton').attr('style', 'display: none');
                console.log("AuthResult code = " + authResult['code']);

                $http({ method: 'POST',
                    url: "http://localhost:9000/storeauthcode",
                    data: {'auth_code' : authResult['code']}, //}$scope.formdata,
                    timeout: 5000,
                    headers: { 'Content-Type' : undefined }
                })
                .success(function(data) {
                    console.log(data);
                    if(data.status === 'OK') {
                        console.log("Saved creds");
                        $scope.signedIn = true;
                    }
                    else {
                        console.log("Could not save creds");
                }
                })
                .error(function(data) {
                    console.log("ERRRRR!");
                });
            } else {
                console.log("Could not save auth code to server");
                // There was an error.
            }
    };

    $scope.signIn = function() {
        console.log("Called signIn");
        $scope.auth2.grantOfflineAccess().then($scope.signInCallback);
    };

    $scope.start = function() {
        console.log("in function start()");
        gapi.load('auth2', function() {
            console.log("in gapi.load()");
            $scope.auth2 = gapi.auth2.init({
            //client_id: 'YOUR_CLIENT_ID.apps.googleusercontent.com',
            client_id:'416430916426-oghsnp3l7kn652a46kiavtqsf15g6bpj.apps.googleusercontent.com',
            // Scopes to request in addition to 'profile' and 'email'
            //scope: 'email'
            });

            console.log($scope.auth2);
        });
    };

    $scope.start(); // call this in the beginning
}]);
*/

/*
function SignInController($scope) {
    // This flag we use to show or hide the button in our HTML.
    $scope.signedIn = false;

    // Here we do the authentication processing and error handling.
    // Note that authResult is a JSON object.
    $scope.processAuth = function(authResult) {
        // Do a check if authentication has been successful.
        if(authResult['access_token']) {
            // Successful sign in.
            $scope.signedIn = true;

            //     ...
            // Do some work [1].
            //     ...
        } else if(authResult['error']) {
            // Error while signing in.
            $scope.signedIn = false;

            // Report error.
        }
    };

    // When callback is received, we need to process authentication.
    $scope.signInCallback = function(authResult) {
        $scope.$apply(function() {
            $scope.processAuth(authResult);
        });
    };

    // Render the sign in button.
    $scope.renderSignInButton = function() {
        gapi.signin.render('signInButton',
            {
                'callback': $scope.signInCallback, // Function handling the callback.
                'clientid': '[CLIENT_ID from Google developer console]', // CLIENT_ID from developer console which has been explained earlier.
                'requestvisibleactions': 'http://schemas.google.com/AddActivity', // Visible actions, scope and cookie policy wont be described now,
                                                                                  // as their explanation is available in Google+ API Documentation.
                'scope': 'https://www.googleapis.com/auth/plus.login https://www.googleapis.com/auth/userinfo.email',
                'cookiepolicy': 'single_host_origin'
            }
        );
    }

    // Start function in this example only renders the sign in button.
    $scope.start = function() {
        $scope.renderSignInButton();
    };

    // Call start function on load.
    $scope.start();
}
*/
