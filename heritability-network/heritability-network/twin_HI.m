function H2=twin_H(rho_MZ, rho_DZ)
% H2=twin_H(rho_MZ, rho_DZ)
%
% Given correlations rho_MZ and rho_DZ, it computes
% the heritability index (HI). 
%
%
%
% (C) Moo K. Chung
%  email://mkchung@wisc.edu
%  Department of Biostatisics and Medical Informatics
%  University of Wisconsin, Madison
%
% Update History: 2015 June 29

%-----------------------------------------------------------

rho_MZ= (rho_MZ+rho_MZ')/2;
rho_DZ= (rho_DZ+rho_DZ')/2;

H2= 2*(rho_MZ- rho_DZ);
H2(H2<0)=0;
H2(H2>1)=1;