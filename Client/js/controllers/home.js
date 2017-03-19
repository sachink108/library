'use strict';

app.controller('HomeController', ['$rootScope','$scope', '$uibModal', '$cookieStore', '$http', function ($scope, $rootScope, $uibModal, $cookieStore, $http) {
    var globals = $cookieStore.get('globals');
    $scope.username = globals.currentUser.username;
    $scope.toggle = true;
    $scope.showHide = "Show Categories";
    
    $scope.toggleCat = function() {
        $("#wrapper").toggleClass("toggled");
        $scope.showHide = $scope.showHide === "Show Categories" ? "Hide Categories" : "Show Categories";
    };

/*
    $scope.readURL = function(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function(e) {
                $('#blah').attr('src', e.target.result)
                    .width(150)
                    .height(200);
            };
            
            reader.readAsDataURL(input.files[0]);
        }
    };
*/    
    $scope.addBook = function() {
        console.log("Adding Book");
        var modalInstance = $uibModal.open({
          animation: $scope.animationsEnabled,
          templateUrl: 'addBook.html',
          controller: 'ModalInstanceCtrl',
          resolve: {
          }
        });
        modalInstance.result.then(function (selectedItem) {

        }, function () {
            console.log('Modal dismissed at: ' + new Date());
        });
    };
}]);

// Later look at this for added functionality
//https://github.com/blueimp/JavaScript-Load-Image
app.controller('ModalInstanceCtrl', function ($scope, $uibModalInstance, $http) {
    $scope.img_file = '';
    $scope.img_data = '';
    $scope.img_file = '';
    $scope.fileData;
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
    
    $scope.readURL = function(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            $scope.img_file = input.files[0];
            reader.readAsDataURL(input.files[0]);
            reader.onload = function(e) {
                $('#blah').attr('src', e.target.result)
                    .width(150)
                    .height(200);
            };
        }
    };
  
    $scope.ok = function () {
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
    };
    
    $scope.cancel = function () {
        $uibModalInstance.dismiss('cancel');
    };
});
