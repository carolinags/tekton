var funcionarioModulo=angular.module('funcionarioModulo',['rest']);

funcionarioModulo.directive('funcionarioform',function(){
    return {
        restrict:'E',
        replace:true,
        templateUrl:'/static/funcionario/html/funcionario_form.html',
        scope:{
            funcionario:'=',
            saveComplete:'&'
        },
        controller:function($scope, FuncionarioApi) {
            $scope.salvandoFlag=false;
            $scope.salvar = function(){
                $scope.salvandoFlag=true;
                $scope.errors={};
                var promessa = FuncionarioApi.salvar($scope.funcionario);
                promessa.success(function(funcionario){
                    $scope.salvandoFlag=false;
                    $scope.funcionario.nome='';
                    $scope.funcionario.email='';
                    $scope.funcionario.telefone='';
                    $scope.funcionario.nascimento='';
                    $scope.funcionario.acesso='';
                    if($scope.saveComplete != undefined) {
                        $scope.saveComplete({'funcionario':funcionario});
                    }
                    $scope.mostrarFormFlag = false;
                })
                    promessa.error(function(erros){
                    $scope.errors=erros;
                    $scope.salvandoFlag=false;
                });
            }
        }
    };
});


funcionarioModulo.directive('funcionariolinha',function(){
    return {
        restrict: 'A',
        replace: true,
        templateUrl: '/static/funcionario/html/funcionario_linha.html',
        scope:{
            funcionario: '=',
            deleteComplete: '&'
        },
        controller:function($scope, FuncionarioApi){
            $scope.ajaxFlag=false;
            $scope.editandoFlag=false;
            $scope.funcionarioEdicao={}
            $scope.deletar=function(){
                FuncionarioApi.deletar($scope.funcionario.id).success(function(){
                    $scope.ajaxFlag=true;
                    $scope.deleteComplete({'funcionario':$scope.funcionario});
                });
            };
            $scope.editar=function(){
                    $scope.editandoFlag=true;
                    $scope.funcionarioEdicao.id=$scope.funcionario.id;
                    $scope.funcionarioEdicao.nome=$scope.funcionario.nome;
                    $scope.funcionarioEdicao.email=$scope.funcionario.email;
                    $scope.funcionarioEdicao.telefone=$scope.funcionario.telefone;
                    $scope.funcionarioEdicao.nascimento=$scope.funcionario.nascimento;
                    $scope.funcionarioEdicao.acesso=$scope.funcionario.acesso;
            };
            $scope.cancelar=function(){
                $scope.editandoFlag=false;
            };

            $scope.completarEdicao=function(){
                FuncionarioApi.editar($scope.funcionarioEdicao).success(function(funcionario){
                    $scope.funcionario=funcionario;
                    $scope.editandoFlag=false;
                });
            }
        }

    };
});