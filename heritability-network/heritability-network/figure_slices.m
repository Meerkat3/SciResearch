function figure_slices(template, seed, name, cscale) 

% figure_slices(template, seed) 
%
% template: 3D brain images
% seed    : seed voxel where images to be shown
% name    : any string, data name by default.
% cscale  : color scale
%
% (c) 2015 Moo K. Chung
% Department of Biostatistics and Medical Informatics
% University of Wisconsin-Madison
% mkchung@wisc.edu
%
% update history
% 2010 Feb. 14 created
% 2014 Sep. 28 fMRI diplay added
% 2014 Nov. 18 colorbar added
% 2015 Feb. 14 title added



%variable length arguments

if nargin<3
    name=[];
end

if nargin<4
    maxt=max(max(max(template)));
    mint=min(min(min(template)));
end

if nargin==4
    maxt=cscale(2);
    mint=cscale(1);
end

x=seed(1);
y=seed(2);
z=seed(3);

figure;
c=20; % fontsize

% box positions
% RECT = [left, bottom, width, height]
%normalized units where (0,0)is the lower-left 
%corner and (1.0,1.0) is the upper-right.
h=0.39; %horizontal gap 
w=0.4; % bottom    
b=0.55; 
bgap=0.03; %bottom gap

dim=size(template);

% x slice
%subplot(1,3,1)
a(1)=axes('position',[0.05 w h*3/4 w]);

ximg = squeeze(template(x,:,:));
ximg90= rot90(ximg);
imagesc(ximg90);
hold on; plot(y,z,'+m','LineWidth',2, 'MarkerSize',15);
caxis([mint maxt]);
axis square; 
axis off;
%colormap('gray');
title(['Sagittal: x = ', int2str(x)],'FontSize',c);

%y slice
%subplot(1,3,2)
a(2)=axes('position',[0.05+w*3/4 w h*3/4 w]); %middle
yimg=squeeze(template(:,y,:));
yimg90= rot90(yimg);
imagesc(yimg90);
hold on; plot(x,z,'+m','LineWidth',2, 'MarkerSize',15);
caxis([mint maxt]);
axis square; 
axis off;
%colormap('gray');
%hold on; plot(z,x,'sr');
title(['Coronal: y = ', int2str(y)],'FontSize',c);

% z slice
%subplot(1,3,3)
a(3)=axes('position',[0.05+1-w w h*3/4 w]); %right
zimg=template(:,:,dim(3)-z);
zimg90= rot90(zimg);
imagesc(zimg90);
hold on; plot(x,dim(2)-y,'+m','LineWidth',2, 'MarkerSize',15);
caxis([mint maxt]);
axis square;
axis off
%colormap('gray');
%hold on; plot(y,x,'sr');
title(['Axial: z = ', int2str(z)],'FontSize',c);


% HORIZONTAL COLORBAR
colormap('jet')
cb=colorbar('location','South');
caxis([mint maxt]);
%set(cb,'Position',[0.05+w*3/4 w-0.05 0.3 0.03]);
set(cb,'Position',[0.05+w*3/4 w-0.1 0.3 0.03]);
set(cb,'XAxisLocation','bottom');
set(gca, 'Fontsize',c);
%axis off

% TITLE
%h=get(cb,'Title');
%a(4)=axes('position',[0.05+w*3/4 w-0.25 0.3 0.03]); %bottom
a(4)=axes('position',[0.05+w*3/4 w-0.3 0.3 0.03]);
axis off;
title(name,'FontSize',c)


set(gcf,'Color','w');
 