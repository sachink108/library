'use strict';

app.controller('HomeController', ['$rootScope','$scope', '$uibModal', '$cookieStore', '$http', 'LibraryService', '$route',
 function ($scope, $rootScope, $uibModal, $cookieStore, $http, LibraryService, $route) {
    var globals = $cookieStore.get('globals');
    $scope.username = globals.currentUser.username;
    $scope.toggle = true;
    $scope.showHide = "Show Categories";
    //$scope.showHide = "Hide Categories";
    $scope.books = [];
    $scope.categories = [];
    $scope.allBooks = [];
    $scope.displayText = "Recently Added Books";
    $scope.searchData = {};
    $scope.book_deleted = false;
    $scope.currentCategory = '';

    $scope.toggleFavourite = function(book) {
        var newvalue = book.favourite === "true" ? "false" : "true";
        book.favourite = newvalue; // update the current books fav value
        var url = 'http://localhost:9000/update/user='+$scope.username+',book_id='+book.id+',field=favourite,value='+book.favourite;
        console.log(url);
        $http({method:'POST',
               url:url,
               timeout: 5000}
              )
              .success(function(data, status, headers, config) {
                if (data.status === "OK") {
                    book.favouriteButtonStyle = book.favourite === "true" ? {'color':'red','border':'none'} : {'color':'grey','border':'none'};
                } else {
                    console.log("eff");
                }
            }).error(function(data, status, headers, config) {
                console.log("error");
            });
    };

    $scope.toggleCurrent = function(book) {
        console.log("In currentlyReading " + book.id);
        // tornado call to add to favourite
        console.log("currently Reading = " + book.currentlyReading);
        if (book.currentlyReading === undefined || book.currentlyReading === false) {
            book.currentlyReading = "true";
            book.currentlyReadingButtonStyle = "color:blue;border:none";
        } else {
            book.currentlyReadingButtonStyle = "color:grey;border:none";
            book.currentlyReading = false;
        }
    };
    $scope.deleteBook = function(id, title, author) {
        console.log("In delete book " + id);
        var url = 'http://localhost:9000/delete/user='+$scope.username+',book_id='+id;
        console.log(url);
        $http({method:'POST',
               url:url,
               timeout: 5000}
              )
              .success(function(data, status, headers, config) {
                if (data.status === "OK") {
                    $scope.alert_text = "Deleted [" + title + " by " + author + "]";
                    $scope.book_deleted = true;
                    $route.reload();
                    //console.log("current category is " + $scope.currentCategory);
                    //$scope.getBooks($scope.currentCategory);
                } else {
                    console.log("eff");
                }
            }).error(function(data, status, headers, config) {
                console.log("error");
            });
    };
    
    $scope.editBook = function(title, author) {
        console.log("In Edit Book");
        $scope.showEditFields = true;
    };

    $scope.search = function() {
        var url = 'http://localhost:9000/search/user='+$scope.username+',query_string='+$scope.searchData.querystring;
        console.log(url);
        $http({method:'GET',
               url:url,
               timeout: 5000}
              )
              .success(function(data, status, headers, config) {
                $scope.books = [];
                for (var book in data.books) {
                    $scope.books.push(data.books[book]);
                }
            }).error(function(data, status, headers, config) {
                console.log("error");
            });
        $scope.displayText = "Search results for '" + $scope.searchData.querystring + "'";
    };

    $scope.getBooks = function(category) {
        var cat = '';
        if(category === '') {
            cat = 'recent';
            $scope.displayText = "Recently Added Books";
        } else {
            cat = category;
            $scope.displayText = category + " Books";
        }

        $scope.currentCategory = cat;
        var url = 'http://localhost:9000/getbooks/user='+$scope.username+',cat='+cat;
        console.log(url);
        $http({method:'GET', 
               url:url,
               timeout: 5000}
              )
              .success(function(data, status, headers, config) {
                // the digest cycle calls this function several times
                // dont know how to get around that
                $scope.books = [];
                $scope.categories = [];
                for (var cat in data.categories) {
                    var catobj = data.categories[cat];
                    $scope.categories.push({"name" : catobj.name, "count": catobj.count});
                }
                for (var cat in data.books) {
                    for (var book in data.books[cat]) {
                        //console.log("Fav from db is " + data.books[cat][book].favourite);
                        //data.books[cat][book].favouriteButtonStyle = data.books[cat][book].favourite === "true" ? "color:red;border:none" : "color:grey;border:none";
                        data.books[cat][book].favouriteButtonStyle = data.books[cat][book].favourite === "true" ? {'color':'red','border':'none'} : {'color':'grey','border':'none'};
                        data.books[cat][book].currentlyReadingButtonStyle = data.books[cat][book].current === "true" ? "color:blue;border:none" : "color:grey;border:none";
                        $scope.books.push(data.books[cat][book]);
                    }
                }
            }).error(function(data, status, headers, config) {
                console.log("error");
            });

    };// end getBooks()
    
    $scope.toggleCat = function() {
        $("#wrapper").toggleClass("toggled");
        $scope.showHide = $scope.showHide === "Show Categories" ? "Hide Categories" : "Show Categories";
        //$scope.showHide = $scope.showHide === "Hide Categories" ? "Show Categories" : "Hide Categories";
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

    $scope.item = {
        star: false,
        favorite: false,
        bookmark: false
  };
}]);

app.directive('buttonFavorite', function() {
    return {
        scope: true,
        restrict: 'E',
        //<button ng-click="toggleFavourite(book)" type="submit" class="btn btn-default btn-sm" ng-style={{book.favouriteButtonStyle}} title="Add to Favourites"><span class="glyphicon glyphicon-heart"></span></button>-->
        //template: '<button class="btn btn-icon"><span class="glyphicon glyphicon-heart" ng-class="{active: item.favorite}"></span></button>', // not needed
        //template: '<button class="btn btn-icon"><span class="glyphicon glyphicon-heart" ng-class="{active: item.favorite}" ng-style="book.favouriteButtonStyle"></span></button>', // works
        template: '<button class="btn btn-icon"><span class="glyphicon glyphicon-heart" ng-style="book.favouriteButtonStyle"></span></button>',
        link: function(scope, elem, attrs) {
            elem.bind('click', function() {
                scope.$apply(function(){
                    scope.toggleFavourite(scope.book);
                    //console.log("after toggle book fav = " + scope.book.favourite);
                });
            });
        }
    };
});

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
