%--------------------------------------------------
%% Heritability Index computation given in the paper:
%
%% Chung, M.K., Vilalta-Gil, V., Lee, H., Rathouz, P.J., Lahey, B.B., Zald, D.H. 
%% 2017 Exact Topological Inference for Paired Brain Networks via Persistent Homology,
%% Information Processing in Medical Imaging (IPMI)
% http://www.stat.wisc.edu/~mchung/papers/chung.2017.IPMI.pdf
%
%
% This code & data are downloaded from http://www.cs.wisc.edu/~mchung/twins
% If you are using the code, please reference Chung et al. (2017).
%
%
% (C) 2017 Moo K. Chung, 
% Universtiy of Wisconsin-Madison   
% mkchung@wisc.edu
%
%
% 2017 May 20. Tested in iMAC (late 2012) with R2016a with 32GB Ram
%----------------------------------------
%Loading data
%This is contrast map obtained fitting GLM in the  SPM package.
%It contains 4D array of variables volMZ (11 pairs of MZ-twins) and volDZ 
%(9 pairs of DZ-twins of the same sex). 
%
%size(volMZ)
%    22    53    63    46
%size(volDZ)
%    18    53    63    46


load twin.mat


    

%----------------------------------------
% Template construction
% Voxels where the contrast values are given are used to construct the network
%
vols= [volMZ;volDZ]; %combine volumes
template = vol_overlap(vols); % computes the overlap probability where contrast values exists.
%Due to image alignment, and due to SPM processing, some voxels in the template does not have
%the contrast values. The processing is done by Vilalta-Gil, V. and Zald, D.H.. 

slice=[27 31 23] % the default image slice, where the contrat maps are showin in Chung et al. (2017)
figure_slices(template,slice)% template image

template(isnan(template))=0; 
template(template<0.7)=0;
template(template>=0.7)=1; %only overlap probability above 0.7 is used as a template.
figure_slices(template,slice)

ind = find(template); %find voxel indexing for tempalte
dim=size(template);
[x y z] = ind2sub(dim, ind);  %ind2sub is used to determine the equivalent subscript values
                              %corresponding to a given single index into an array.
coord = [x y z];  %this is the voxel coordinates corresponding voxel indexing ind.

%These numbers will likely to change depending on what MATLAB version 
%and operating system you use. 55724 nodes are obtained for Dr. Chung's computer
%
%Options: Here are other possible number of nodes that can be used.
%25972 nodes if image intersection is used. Instead of the overlap probability, only voxels where
%all the contrast values are present are used. Chung et al (2017) computation is based on this.
%55585 nodes if overlap probability is used with 0.7 threshold in new iMac(late 2015) with R2016a.
%50275 nodes if union is used with 0.9 threshold

%---------------------------------------
%Cross correlation in the template voxels only. 
%We don'compute it in the empty space. 
%This saves significant amount of computer memory.


d=size(volMZ); %[d(2) d(3) d(4)] is image size; d(1) number of subjects
volMZ = reshape(volMZ,d(1), d(2)*d(3)*d(4));
d=size(volDZ); %[d(2) d(3) d(4)] is image size; d(1) number of subjects
volDZ = reshape(volDZ,d(1), d(2)*d(3)*d(4));

%The ordering of twins have to be restructured and paired.
twinMZ1 = volMZ(1:2:end,ind);  
twinMZ2 = volMZ(2:2:end,ind); %twinMZ1(1,:) and twinMZ(1,:) are twins. 

twinDZ1 = volDZ(1:2:end,ind);  
twinDZ2 = volDZ(2:2:end,ind); %twinMZ1(1,:) and twinMZ(1,:) are twins. 

%Cross-correlation matrix computation. Corss-correlations are not symmetric.
%The following computation may take 1-2 min per correlation matrix. 
corrMZ = corr2fast(twinMZ1, twinMZ2);
corrDZ = corr2fast(twinDZ1, twinDZ2);

%WARNING: Unless you have huge memory and fast computer, please do not 
%display the whole correlation matrices. Matlab will freeze.
%reduce the size by 1/100th. 
smallMZ = corrMZ(1:100:end,1:100:end);
smallDZ = corrDZ(1:100:end,1:100:end);
figure; imagesc(smallMZ); colorbar
figure; imagesc(smallDZ); colorbar

%Network level heritability index. 
%WARNING: Unless you have a computer with huge RAM,
%do not run it for the full scale correlation matrices corrMZ and corrDZ.
%So we will only show small subsampled regions.
HI = twin_HI(smallMZ, smallDZ);
figure; imagesc(HI); colorbar
