var app = angular.module('takeWing', ['ngMaterial', 'ui.router']).config(function($mdThemingProvider) {
  $mdThemingProvider.theme('default')
	.dark()
});

	app.config(function($stateProvider, $urlRouterProvider){
		$urlRouterProvider.otherwise('/landing')
		
		$stateProvider
			.state('landing', {
				url: '/landing',
				templateUrl: angular_url+'/views/landing.html',
				controller: 'landingCtrl',
				controllerAs: 'ldCtrl'
			})
	});