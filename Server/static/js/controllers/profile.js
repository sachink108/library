'use strict';

app.controller('ProfileController', ['$scope', '$http', '$rootScope', '$cookieStore', '$location',
               function($scope, $http, $rootScope, $cookieStore, $location) {

    var globals = $cookieStore.get('globals');
    console.log("In Profile controller " + globals);
    $scope.userProfile = globals.userProfile;

    $scope.init = function() {
        console.log(globals);
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

