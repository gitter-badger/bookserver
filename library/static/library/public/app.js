var app = angular.module('takeWing', ['ngMaterial', 'ui.router']).config(function($mdThemingProvider) {
  $mdThemingProvider.theme('default')
	.primaryPalette('teal')
	.accentPalette('pink')
});

	app.config(function($stateProvider, $urlRouterProvider){
		$urlRouterProvider.otherwise('/landing')
		
		$stateProvider
			.state('landing', {
				url: '/landing',
				// templateUrl: angular_url+'/views/landing.html', // this needs to be uncommented for production
            templateUrl: "bookserver/library/static/library/public/views/landing.html", // this is for local testing
				controller: 'landingCtrl',
				controllerAs: 'ldCtrl'
			})
	});