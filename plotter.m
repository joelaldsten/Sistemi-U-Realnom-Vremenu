data = load('GUI/data.csv');

x_ref = 0.04;
y_ref = -1.3;

close all;
x = data(:,1);
y = data(:,2);
theta = data(:,3);
u1 = data(:,4);
u2 = data(:,5);
u3 = data(:,6);


length_x = size(data,1);

start_idx = 0;
for i = 1:length_x
    if (u1(i) ~= 0 || u2(i) ~= 0 || u3(i) ~= 0)
        start_idx = i;
        break;
    end
end

stop_idx = 0;
for i = start_idx:length_x
    if (u1(i) == 0 && u2(i) == 0 && u3(i) == 0)
        stop_idx = i;
        break;
    end
end



figure
plot(x,'LineWidth',2)
hold on
plot(y,'LineWidth',2)
plot(theta,'LineWidth',2)
legend('x','y','theta')

x = x(start_idx:stop_idx);
y = y(start_idx:stop_idx);
theta = theta(start_idx:stop_idx);

u1 = u1(start_idx:stop_idx);
u2 = u2(start_idx:stop_idx);
u3 = u3(start_idx:stop_idx);


L = length(x);
e = zeros(L,1);

for i = 1:L
    e(i) = sqrt((x_ref - x(i))^2 + (y_ref - y(i))^2);
end

time = (0:L-1) * 0.2;

figure
plot(time, e,'LineWidth',2)
xlabel('Time [s]')
title('Distance to reference point','FontSize',18)


figure
plot(time,u1,'LineWidth',2)
hold on
plot(time,u2,'LineWidth',2)
plot(time,u3,'LineWidth',2)
xlabel('Time [s]')
title('Control signals','FontSize',18)
legend('u1','u2','u3','FontSize',14)

figure
plot(time,theta,'LineWidth',2)
ylim([-pi,pi])
ylabel('Angle [rad]')
xlabel('Time [s]')
title('Omnibot relative angle','FontSize',18)


xmin = -1.75;
xmax = 1.35;
ymin = -2.2;
ymax = 0.9;
figure
plot(x,y,'LineWidth',2)
grid on
hold on
scatter(x(1),y(1),'go','filled')
scatter(x_ref,y_ref,'ro','filled')
title('Omnibot path','FontSize',18)
xlim([xmin, xmax]);
ylim([ymin, ymax]);
xlabel('x')
ylabel('y')
legend('Path','Starting point','Reference point','FontSize',14)


