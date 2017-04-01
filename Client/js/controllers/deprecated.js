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