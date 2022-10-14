% Create plot with total network capacity

cpe = [10, 50, 100, 300, 600];

req = [30, 100, 300, 500]/1000;
share = [30,30, 30,  10];

uc1 = 0.3*cpe;
uc2 = sum(share/100.*req)*cpe;

figure('Color','w','Name','required network capacity')
hold on;
plot(cpe,uc1, 'd-','DisplayName','Use case 1');
plot(cpe,uc2, 'o-.','DisplayName','Use case 2');
xlabel('Number of CPE devices')
ylabel('Required total capacity of all CPEs [Gbps]')
legend('show','Location','northwest')
