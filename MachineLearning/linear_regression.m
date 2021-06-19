% 60171660 조은학
%% Initialization
clear all; close all; clc

%% a : warming up
% Plot cos(x) praph.
%% ------------your code---------------

figure;

x = 1:0.1:10;
plot(x,cos(x));

%% ------------  end     --------------
pause;


%% b : load data from "hw7data.txt"
%% ------------your code---------------
data = csvread('hw11data.txt')

%% ------------  end     --------------


%% c : split data
%% ------------your code---------------
x = data(:, 1)
y = data(:, 2)

%% ------------  end     --------------
m = length(y);

%% d : plot
%% ------------your code---------------

plot(x, y, 'rx', 'MarkerSize', 4);


%% ------------  end     --------------

fprintf("go to next step using enter key.\n")
pause;

%% e, f : cost function and gradient decent
X = [ones(m, 1), data(:,1)];
theta = zeros(2, 1); 

%% e : define computeCost function
function cost = computeCost(X, y, theta)
%% ------------your code---------------
	m = length(y); %행의 개수 연산
	cost=0;
	hx=0;
  
	for i=1:m % h(x)를 위해((세타1x+세타0)-y)^2을 1부터 m까지 더하는 연산
		hx=hx+(theta(1)+theta(2)*X(i,2)-y(i))^2;
	end
  
	cost=hx/(2*m); %2m으로 나누는 연산

%% ------------  end     --------------
end

%% 반복 회수 및 alpha는 원하는 값으로 수정하여 사용 가능합니다.
iterations = 1500;
alpha = 0.01;

% compute and display initial cost
computeCost(X, y, theta)

fprintf("go to next step using enter key.\n")
pause;

%% f : define fradient decent
%% theta는 학습된 theta, history는 전체 학습 과정을 plotting 할 수 있도록 구현하시오.

function [theta, history] = gradientDescent(X, y, theta, alpha, num_iters)
m = length(y);
history = zeros(num_iters, 1);

%% ------------your code---------------
%iterations개수(1500회)만큼 반복하여 cost function이 최소가 되게하는 값을 찾는다
for t=1:num_iters 
        temp0=0;
        temp1=0;
        for i=1:m%동시에 업데이트, 위의 cost function 적용
            temp0=temp0+(theta(1)+theta(2)*X(i,2)-y(i));
            temp1=temp1+(theta(1)+theta(2)*X(i,2)-y(i))*X(i,2);
        end
        theta(1)=theta(1)-alpha*(temp0/m);%temp를 행의 개수 m으로 나누어 세타0값에 적용
        theta(2)=theta(2)-alpha*(temp1/m);%temp를 행의 개수 m으로 나누어세타1값에 적용
        
        %history의 j번째에 cost function을 계산한 값을 넣는다
        history(t) = computeCost(X, y, theta);
    end
%% ------------  end     --------------

end


fprintf("running......\n")
[theta, history] = gradientDescent(X, y, theta, alpha, iterations);

% 이전에 그린 데이터에 학습한 결과 그리기
hold on;
plot(X(:,2), X*theta, '-')
legend('Training data', 'Linear regression')
hold off;


% g : predict

%% ------------your code---------------
predict1 = [1,20]*theta
predict2 = [1,5.5]*theta
%% ------------  end     --------------


fprintf('For x = 20, we predict %f\n', predict1);
fprintf('For x = 5.5, we predict %f\n', predict2);
fprintf("go to next step using enter key.\n")
pause;

%% 전체 학습 과정에서의 Cost 변화 plotting 하기
figure;
plot([1:iterations], history)
xlabel('num of iterations')
ylabel('Cost')
fprintf("go to next step using enter key.\n")
pause;
