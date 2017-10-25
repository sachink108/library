'use strict';

/*
app.controller('LoginController', ['$scope', '$http', '$rootScope', '$location', 'AuthenticationService',
               function($scope, $http, $rootScope, $location, AuthenticationService) {
    AuthenticationService.ClearCredentials(); // reset login status

    $scope.login = function() {
        $scope.dataLoading = true;
        console.log("Sending to authenticate");
        AuthenticationService.Login($scope.username, $scope.password, function(response) {
            if(response.status === 'success') {
                AuthenticationService.SetCredentials($scope.username, $scope.password);
                $location.path('/home'); // if login is successfull, load this page
            } else {
                $scope.error = "Invalid Username or Password";
                $scope.dataLoading = false;
            }
        });
        //$location.path('/home');
    };
}]);
*/

app.controller('LoginController', ['$scope', '$http', '$rootScope', '$cookieStore', '$location', 'AuthenticationService',
               function($scope, $http, $rootScope, $cookieStore, $location, AuthenticationService) {
    $scope.auth2 = {};
    $scope.authResult;

    /**
    * This method sets up the sign-in listener after the client library loads.
    */
    $scope.signOut = function() {
        console.log("Sign out");
        gapi.auth2.getAuthInstance().signOut();
    };

    $scope.startApp = function(operation) {
        console.log("In Start App : " + operation);
        // This part is dicey, not sure if it works well or at all
        if (operation === 'logoff') {
            if (gapi.auth2.getAuthInstance()) {
                gapi.auth2.getAuthInstance().signOut();
                console.log("we are signed in, so signing out now");
            }
        }
        gapi.load('auth2', function() {
            gapi.client.load('plus','v1').then(function() {
                gapi.signin2.render('signin-button', {
                    scope: 'https://www.googleapis.com/auth/plus.login',
                    fetch_basic_profile: false });

                gapi.auth2.init({fetch_basic_profile: false,
                    scope:'https://www.googleapis.com/auth/plus.login'}).then(
                    function () {
                        // no use storing this auth2 in scope
                        $scope.auth2 = gapi.auth2.getAuthInstance();
                        gapi.auth2.getAuthInstance().isSignedIn.listen($scope.updateSignIn);
                        gapi.auth2.getAuthInstance().then($scope.updateSignIn);
                    });
            });
        });
    };

    /**
    * Handler for when the sign-in state changes.
    *
    * @param {boolean} isSignedIn The new signed in state.
    */
    $scope.updateSignIn = function() {
        //console.log('update sign in state');
        if ($scope.auth2.isSignedIn.get()) {
            console.log('signed in');
            $scope.onSignInCallback(gapi.auth2.getAuthInstance());
        }else{
            console.log('signed out');
            $scope.onSignInCallback(gapi.auth2.getAuthInstance());
            // go back to the sign in page here, make visible default stuff
        }
    };

     /**
     * Hides the sign in button and starts the post-authorization operations.
     *
     * @param {Object} authResult An Object which contains the access token and
     *   other authentication information.
     */
    $scope.onSignInCallback = function(authResult) {
        /*
        $('#authResult').html('Auth Result:<br/>');
        for (var field in authResult) {
            $('#authResult').append(' ' + field + ': ' +
                authResult[field] + '<br/>');
        }
        */
        $scope.authResult = authResult;
        if (authResult.isSignedIn.get()) {
            /*
            $('#authOps').show('slow');
            $('#gConnect').hide();
            $scope.profile();
            $scope.people();
            */
            gapi.client.plus.people.get({
                'userId': 'me'
            }).then(function(res) {
                console.log("User profile is ");
                $rootScope.globals = { userProfile : res.result};
                $cookieStore.put('globals', $rootScope.globals);
                //console.log($rootScope.globals.userProfile);
                console.log("Sign in successfull, loading home page now");
                $location.path('/home'); // if login is successfull, load this page
                $scope.$apply(); // this works with the above
            });
            //console.log("Sign in successfull, loading home page now");
            //$location.path('/home'); // if login is successfull, load this page
            //$scope.$apply(); // this works with the above
        } else {
            if (authResult['error'] || authResult.currentUser.get().getAuthResponse() == null) {
                // There was an error, which means the user is not signed in.
                // As an example, you can handle by writing to the console:
                console.log('There was an error: ' + authResult['error']);
            }
            //$('#authResult').append('Logged out');
            //$('#authOps').hide('slow');
            //$('#gConnect').show();
        }
        //console.log('authResult', authResult);
    };

    /**
     * Calls the OAuth2 endpoint to disconnect the app for the user.
     */
    $scope.disconnect = function() {
        //console.log("Disconnect")
        // Revoke the access token.
        gapi.auth2.getAuthInstance().disconnect();
        // lot more has to happen here -
        // delete user account from elastic search?
        // set expiration date on the account - acc will be deleted 3 months after disonnection?
    };

    /**
     * Gets and renders the list of people visible to this app.
     */
     // get info from the function later
    $scope.people = function() {
        gapi.client.plus.people.list({
            'userId': 'me',
            'collection': 'visible'
        }).then(function(res) {
            var people = res.result;
            $('#visiblePeople').empty();
            $('#visiblePeople').append('Number of people visible to this app: ' +
            people.totalItems + '<br/>');
            for (var personIndex in people.items) {
                person = people.items[personIndex];
                $('#visiblePeople').append('<img src="' + person.image.url + '">');
            }
        });
    };

     /**
     * Gets and renders the currently signed in user's profile data.
     */
    $scope.profile = function() {
        gapi.client.plus.people.get({
            'userId': 'me'
        }).then(function(res) {
            var profile = res.result;
            console.log(profile);
            //$('#profile').empty();
            $('#profile').append(
            $('<p><img src=\"' + profile.image.url + '\"></p>'));
            $('#profile').append(
            $('<p>Hello ' + profile.displayName + '!<br />Tagline: ' +
            profile.tagline + '<br />About: ' + profile.aboutMe + '</p>'));
            if (profile.emails) {
                $('#profile').append('<br/>Emails: ');
                for (var i=0; i < profile.emails.length; i++) {
                    $('#profile').append(profile.emails[i].value).append(' ');
                }
                $('#profile').append('<br/>');
            }
            if (profile.cover && profile.coverPhoto) {
                $('#profile').append(
                $('<p><img src=\"' + profile.cover.coverPhoto.url + '\"></p>'));
            }
        }, function(err) {
            var error = err.result;
            $('#profile').empty();
            $('#profile').append(error.message);
        });
    };
}]);

