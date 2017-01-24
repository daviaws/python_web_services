angular.module('app', []).controller('index', index);

function index($scope, $http) {
    $scope.request = {};
    $scope.state = 0;
    $scope.result = 0;
    $scope.action = "";
    $scope.select_state = "";
    $scope.insert_state = "";
    $scope.delete_state = "";

    $scope.send_http = function (method, route) {
        $http({
            url: window.location.origin + route,
            method: method,
            data: $scope.request
            }).success(function(data) {
                console.log(data);
            })
            .error(function(data) {
                console.log("Error on request: " + data);
            });
    }

    $scope.do_request = function () {
        var route = '/db/person';
        var cpf = $scope.request.cpf;
        if($scope.action == 'select') {
            if(cpf != "*") {
                route = route + '/' + cpf;
            }
            $scope.send_http('GET', route);
        } else if ($scope.action == 'insert') {
            $scope.send_http('PUT', route);
        } else if ($scope.action == 'delete') {
            if(cpf != "*") {
                route = route + '/' + cpf;
            }
            $scope.send_http('DELETE', route);
        } else {
            alert("Nothing to do");
        }
    }

    $scope.changeSelector = function (select) {
        if(select == 'select') {
            $scope.select_state = "btn-primary";
            $scope.insert_state = "";
            $scope.delete_state = "";
            $scope.action = "select";
            $scope.state = 1;
        } else if (select == 'insert') {
            $scope.select_state = "";
            $scope.insert_state = "btn-primary";
            $scope.delete_state = "";
            $scope.action = "insert";
            $scope.state = 2;
        } else if (select == 'delete') {
            $scope.select_state = "";
            $scope.insert_state = "";
            $scope.delete_state = "btn-primary";
            $scope.action = "delete";
            $scope.state = 1;
        } else {
            $scope.select_state = "";
            $scope.insert_state = "";
            $scope.delete_state = "";
            $scope.action = "";
            $scope.state = 0;
            $scope.request = {};
        }
    }
}
