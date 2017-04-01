'use strict';

app.controller('HomeController', ['$rootScope','$scope', '$uibModal', '$cookieStore', '$http', 'LibraryService',
 function ($scope, $rootScope, $uibModal, $cookieStore, $http, LibraryService) {
    var globals = $cookieStore.get('globals');
    $scope.username = globals.currentUser.username;
    $scope.toggle = false;
    $scope.showHide = "Show Categories";
    $scope.books = [];
    $scope.categories = [];
    $scope.allBooks = [];
    $scope.displayText = "Recently Added Books";
    
    $scope.deleteBook = function(title, author) {
        console.log("In delete book");
    };
    
    $scope.editBook = function(title, author) {
        console.log("In Edit Book");
        $scope.showEditFields = true;
    };
    
    $scope.getBooks = function(category) {
        $http({method:'GET', 
               url:'http://localhost:9000/getbooks', 
               timeout: 5000}
              )
              .success(function(data, status, headers, config) {
                // the digest cycle calls this function several timss
                // dont know how to get around that
                $scope.books = [];
                $scope.allBooks = data.catWiseBooks;
                $scope.categories = [];
                for (var cat in data.catWiseBooks) {
                    $scope.categories.push({"name" : cat, "count": data.catWiseBooks[cat].length});
                }
                if (category === '') {
                    $scope.books = $scope.books = data.recent.recent;
                } else {
                    $scope.displayText = category + " Books";
                    $scope.books = data.catWiseBooks[category];
                }
            }).error(function(data, status, headers, config) {
                console.log("error");
            });
    };// end getBooks()
    
    $scope.toggleCat = function() {
        $("#wrapper").toggleClass("toggled");
        $scope.showHide = $scope.showHide === "Show Categories" ? "Hide Categories" : "Show Categories";
    };

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
    
   $scope.getBooks('');
   /*
    // tried to do something like this to circumvent
    // the effect of the digest cycle which calls
    // getBooks() repeatedly, but it did not work
    LibraryService.GetBooks(function(response) {
        console.log(response);
        if(response.status) {
            console.log("inCallback");
        } else {
            console.log("Could not getBooks");
        }
    });
    */
}]);

app.directive('ngFiles', ['$parse', function ($parse) {
    function fn_link(scope, element, attrs) {
                var onChange = $parse(attrs.ngFiles);
                element.on('change', function (event) {
                    onChange(scope, { $files: event.target.files });
                });
            };

    return {
        link: fn_link
        }
} ]);

// Later look at this for added functionality
//https://github.com/blueimp/JavaScript-Load-Image
app.controller('ModalInstanceCtrl', function ($scope, $uibModalInstance, $http) {
    $scope.formdata = new FormData();
    
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

    $scope.getTheFiles = function ($files) {
        console.log("IN GET THE FILES");
        console.log($files);
        angular.forEach($files, function (value, key) {
            $scope.formdata.append(key, value);
            console.log(key + ' ' + value.name);
        });
    };

    $scope.ok = function () {
        $scope.formdata.append("username", $scope.username);
        $scope.formdata.append("title", $scope.title);
        $scope.formdata.append("author", $scope.author);
        $scope.formdata.append("category", $scope.category);

        console.log("Sending " + $scope.formdata);
        $http({ method: 'POST', 
                url: "http://localhost:9000/addbook",
                data: $scope.formdata,
                timeout: 5000,
                headers: { 'Content-Type' : undefined },
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
    
    $scope.cancel = function () {
        $uibModalInstance.dismiss('cancel');
    };
});
