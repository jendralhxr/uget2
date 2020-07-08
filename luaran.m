fps= 60;
time=0:1/fps:size(data,1)/fps-0.001;

[short count] =movavg(data(:,1),1,300);
plot(time,count);
xlabel("time (s)");
ylabel("active cells count");
print("activecells.png");

[short density] =movavg(data(:,5),1,300);
plot(time,density);
xlabel("time (s)");
ylabel("density index (cells/radius)");
print("density.png");

clear heatmap_sepi;
heatmap_sepi(640,480)= 0;
t_start = 1;
t_stop  = 1800; # 30 detik pertama
for (t=t_start:t_stop)
	heatmap_sepi(floor(data(t,2)	), floor(data(t,3))    	) += 4;
	heatmap_sepi(floor(data(t,2)	), floor(data(t,3))-1  	) += 2;
	heatmap_sepi(floor(data(t,2)	), floor(data(t,3))+1  	) += 2;
	heatmap_sepi(floor(data(t,2)+1	), floor(data(t,3))  	) += 2;
	heatmap_sepi(floor(data(t,2)+1	), floor(data(t,3))  	) += 2;
	heatmap_sepi(floor(data(t,2)-1	), floor(data(t,3))-1	) += 1;
	heatmap_sepi(floor(data(t,2)-1	), floor(data(t,3))+1	) += 1;
	heatmap_sepi(floor(data(t,2)+1	), floor(data(t,3))-1	) += 1;
	heatmap_sepi(floor(data(t,2)+1	), floor(data(t,3))+1	) += 1;
endfor
pcolor(heatmap_sepi);
shading flat;
colorbar;
caxis([0 120])
title(sprintf("heatmap t=0 to 30 s",t/60));
print("heatmap sepi.png");

clear heatmap_rame;
heatmap_rame(640,480)= 0;
t_start = 5401;
t_stop  = 7200; # 30 detik pertama
for (t=t_start:t_stop)
	heatmap_rame(floor(data(t,2)	), floor(data(t,3))    	) += 4;
	heatmap_rame(floor(data(t,2)	), floor(data(t,3))-1  	) += 2;
	heatmap_rame(floor(data(t,2)	), floor(data(t,3))+1  	) += 2;
	heatmap_rame(floor(data(t,2)+1	), floor(data(t,3))  	) += 2;
	heatmap_rame(floor(data(t,2)+1	), floor(data(t,3))  	) += 2;
	heatmap_rame(floor(data(t,2)-1	), floor(data(t,3))-1	) += 1;
	heatmap_rame(floor(data(t,2)-1	), floor(data(t,3))+1	) += 1;
	heatmap_rame(floor(data(t,2)+1	), floor(data(t,3))-1	) += 1;
	heatmap_rame(floor(data(t,2)+1	), floor(data(t,3))+1	) += 1;
endfor
pcolor(heatmap_rame);
shading flat;
colorbar;
caxis([0 120])
title(sprintf("heatmap t=90 to 120 s",t/60));
print("heatmap rame.png");

