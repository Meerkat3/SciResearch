function vol =vol_overlap(vols)
% vol =vol_overlap(vols)
%
% Given a collection of 3D volumes, it computes the overlap probability
% where image intensity values are given. 
%
%
%
% (C) Moo K. Chung
%  email://mkchung@wisc.edu
%  Department of Biostatisics and Medical Informatics
%  University of Wisconsin, Madison
%
% Update History: 2016 May 29 created
% 2017 May 19 modified from volume_union.m
%-----------------------------------------------------------

d=size(vols);

n=d(1);  % number of images
dim=d(2:4); %image dimesion
        
slices=zeros(dim(1),dim(2), n); 
vol=zeros(dim(1),dim(2),dim(3));

for k=1:dim(3)
    %computing slice by slice
    for j=1:n
      slices(:,:,j)=vols(j,:,:,k);  %j-th image, k-th slice
    end;
    
    %slice is k-th image slice for all subjects
      
    temp = reshape(slices, dim(1)*dim(2),n);
    temp = ~isnan(temp);
    temp = sum(temp,2)/n;
    
    vol(:,:,k) = reshape(temp, dim(1), dim(2));
    
end