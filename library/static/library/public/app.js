var app = angular.module('takeWing', ['ngMaterial', 'ui.router']);

	app.config(function($stateProvider, $urlRouterProvider){
		$urlRouterProvider.otherwise('/landing')
		
		$stateProvider
			.state('landing', {
				url: '/landing',
				templateUrl: 'views/landing.html',
				controller: 'landingCtrl',
				controllerAs: 'ldCtrl'
			})
	});