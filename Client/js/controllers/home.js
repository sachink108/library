'use strict';

app.controller('HomeController', ['$rootScope','$scope', '$uibModal', '$cookieStore', '$http', function ($scope, $rootScope, $uibModal, $cookieStore, $http) {
    var globals = $cookieStore.get('globals');
    $scope.username = globals.currentUser.username;
    $scope.toggle = false;
    $scope.showHide = "Show Categories";
    $scope.catetories = [];
    $scope.books = [];
    $scope.displayText = "Recently Added Books";
    
    $scope.getCategories = function() {
        console.log("get categories");
        // $htt get here
        $scope.categories = [{"name" : "Action", "count": 20},
                        {"name" : "Spiritual", "count": 12},
                        {"name" : "Autobiography", "count": 5},
                        {"name" : "Thriller", "count": 10},
                        ];
    };
    
    $scope.getBooks = function(category) {
        if (category === '') {
            // get recently added books
            console.log("getting recently added books");
        } else {
            $scope.displayText = category + " Books";
            // http get books on categories
            console.log("getting books of category " + category);
        }
        
        $scope.books = [
            {"author" : "Lee Child",
            "title" : "The Visitor",
            "img": "sachin/f866bc97-3068-488d-b48f-22cf6007a203.jpg"},
            {"author" : "Sidney Sheldon",
            "title" : "Master of the Game",
            "img": "sachin/0576b851-89b6-4d82-ae3a-8b28d53613fd.jpg"},
            ];
    };
    
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
    
    $scope.getCategories();
    $scope.getBooks('');
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
