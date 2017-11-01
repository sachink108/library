'use strict';

app.controller('HomeController', ['$rootScope','$scope', '$uibModal', '$cookieStore', '$http', 'LibraryService', '$route',
 function ($scope, $rootScope, $uibModal, $cookieStore, $http, LibraryService, $route) {
    var globals = $cookieStore.get('globals');
    console.log("In Home controller " + globals);
    $scope.userProfile = globals.userProfile;

    $scope.displayName = $scope.userProfile.displayName;
    $scope.givenName = $scope.userProfile.name.givenName;
    $scope.username = $scope.displayName.replace(/ /g, '_');
    $scope.userGoogleID = $scope.userProfile.id;
    $scope.displayImageURL = $scope.userProfile.image.url;

    $scope.inRefresh = false;
    $scope.showHide = "Show Categories";
    $scope.books = [];
    $scope.categories = [];
    $scope.allBooks = [];
    $scope.displayText = "Recently Added Books";
    $scope.searchData = {}; // data need to be wrapped inside this object to reflect here
    $scope.book_deleted = false;
    $scope.currentCategory = '';
    $scope.fav_count = 0;
    $scope.cur_count = 0;

    $scope.toggleFavourite = function(book) {
        var newvalue = book.favourite === "true" ? "false" : "true";
        book.favourite = newvalue; // update the current books fav value
        //var url = 'http://localhost:9000/update/user='+$scope.username+',book_id='+book.id+',field=favourite,value='+book.favourite;
        var url = 'http://localhost:9000/update/user='+$scope.userGoogleID+',book_id='+book.id+',field=favourite,value='+book.favourite;
        console.log(url);
        $http({method:'POST', url:url, timeout: 5000})
              .success(function(data, status, headers, config) {
                if (data.status === "OK") {
                    setFavouriteButtonStyle(book);
                    if (newvalue === "false") {
                        $scope.fav_count -= 1;
                    }
                    //book.favouriteButtonStyle = book.favourite === "true" ? {'color':'red','border':'none'} : {'color':'grey','border':'none'};
                } else {
                    console.log("could not set favorite");
                }
            }).error(function(data, status, headers, config) {
                console.log("could not set favourite");
            });
    };

    $scope.toggleCurrent = function(book) {
        var newvalue = book.current === "true" ? "false" : "true";
        book.current = newvalue; // update the current books current value
        var url = 'http://localhost:9000/update/user='+$scope.userGoogleID+',book_id='+book.id+',field=current,value='+book.current;
        console.log(url);
        $http({method:'POST', url:url, timeout: 5000})
              .success(function(data, status, headers, config) {
                if (data.status === "OK") {
                    setCurrentButtonStyle(book);
                    if (newvalue === "false") {
                        $scope.cur_count -= 1;
                    }
                    //book.currentButtonStyle = book.current === "true" ? {'color':'blue','border':'none'} : {'color':'grey','border':'none'};
                } else {
                    console.log("could not set current");
                }
            }).error(function(data, status, headers, config) {
                console.log("error");
            });
    };

    $scope.deleteBook = function(id, title, author) {
        var url = 'http://localhost:9000/delete/user='+$scope.userGoogleID+',book_id='+id;
        console.log(url);
        $http({method:'POST', url:url, timeout: 5000})
              .success(function(data, status, headers, config) {
                if (data.status === "OK") {
                    $scope.alert_text = "Deleted [" + title + " by " + author + "]";
                    $scope.book_deleted = true;
                    $route.reload();
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
        var url = 'http://localhost:9000/search/user='+$scope.userGoogleID+',query_string='+$scope.searchData.querystring;
        console.log(url);
        $http({method:'GET', url:url, timeout: 5000})
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

    var setFavouriteButtonStyle = function(book) {
        if (book.favourite === "true") {
            book.favouriteButtonStyle = {'color':'red','border':'none'};
            return 1;
        }else {
            book.favouriteButtonStyle = {'color':'grey','border':'none'};
            return 0;
        }
    };

    var setCurrentButtonStyle = function(book) {
        if (book.current === "true") {
            book.currentButtonStyle = {'color':'blue','border':'none'};
            return 1;
        }else {
            book.currentButtonStyle = {'color':'grey','border':'none'};
            return 0;
        }
    };

    $scope.getBooks = function(category) {
        var cat = '';
        if (category === '') {
            category = 'recent';
            $scope.displayText = "Recently Added Books";
        }else if (category === 'favorite') {
            $scope.displayText = "Favorite Books";
        } else if (category === 'current') {
            $scope.displayText = "Currently Reading Books";
        }else {
            $scope.displayText = category + " Books";
        }

        $scope.currentCategory = category;
        var url = 'http://localhost:9000/getbooks/user='+$scope.userGoogleID+',cat='+category;
        console.log(url);
        $http({method:'GET', url:url, timeout: 5000})
              .success(function(data, status, headers, config) {
                //if (data.status === 'OK') {
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
                            $scope.fav_count += setFavouriteButtonStyle(data.books[cat][book]);
                            $scope.cur_count += setCurrentButtonStyle(data.books[cat][book]);
                            $scope.books.push(data.books[cat][book]);
                        }
                    }
                //} else {
                //    console.log("No Books found!!"); // shhow a div with apt message or something
                //}
            }).error(function(data, status, headers, config) {
                console.error("some other error");
            });
    };// end getBooks()
    
    $scope.toggleCat = function() {
        $("#wrapper").toggleClass("toggled");
        //$("#wrapper").toggleClass("active");
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
}]);

//http://seanhess.github.io/2013/10/14/angularjs-directive-design.html
app.directive('buttonFavorite', function() {
    return {
        scope: true,
        restrict: 'E',
        template: '<button class="btn btn-icon"><span class="glyphicon glyphicon-heart" ng-style="book.favouriteButtonStyle"></span></button>',
        link: function(scope, elem, attrs) {
            elem.bind('click', function() {
                scope.$apply(function(){
                    scope.toggleFavourite(scope.book);
                });
            });
        }
    };
});

app.directive('buttonCurrent', function() {
    return {
        scope: true,
        restrict: 'E',
        template: '<button class="btn btn-icon"><span class="glyphicon glyphicon-bookmark" ng-style="book.currentButtonStyle"></span></button>',
        link: function(scope, elem, attrs) {
            elem.bind('click', function() {
                scope.$apply(function(){
                    scope.toggleCurrent(scope.book);
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
        console.log($files);
        angular.forEach($files, function (value, key) {
            $scope.formdata.append(key, value);
            console.log(key + ' ' + value.name);
        });
    };

    $scope.ok = function () {
        $scope.formdata.append("user_id", $scope.userGoogleID);
        $scope.formdata.append("title", $scope.title);
        $scope.formdata.append("author", $scope.author);
        $scope.formdata.append("category", $scope.category);

        console.log("Uploading book ");
        $http({ method: 'POST', 
                url: "http://localhost:9000/addbook",
                data: $scope.formdata,
                timeout: 10000,
                headers: { 'Content-Type' : undefined },
        })
        .success(function(data) {
            console.log(data);
            if(data.status === 'OK') {
                console.log("Added book successfully.");
                $uibModalInstance.close();
            }
            else {
                console.error("Failed to add book");
            }
        })
        .error(function(data) {
            console.error("Error in Add Book!");
        });
    };
    
    $scope.cancel = function () {
        $uibModalInstance.dismiss('cancel');
    };
});
