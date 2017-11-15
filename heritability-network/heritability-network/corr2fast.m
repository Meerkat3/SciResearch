function C = corr2fast(X,Y);
%
% function C = corr2fast(X,Y);
%
% Extremply fast cross-correlation computation for n x p data matrices X and Y.
% If n and m are bigger than 25000, you need to break up the matrix.
% For reference for this function, see
%
% Chung, M.K., Hanson, J.L., Ye, J., Davidson, R.J. Pollak, S.D. 2015 
% Persistent Homology in Sparse Regression and Its Application to Brain Morphometry. 
% IEEE Transactions on Medical Imaging, 34:1928-1939
% http://www.stat.wisc.edu/~mchung/papers/chung.2015.TMI.pdf
%
% (C) Moo K. Chung
%  email://mkchung@wisc.edu
%  Department of Biostatisics and Medical Informatics
%  University of Wisconsin, Madison
%
%
% Update History: 
%       2015 Oct. 28 created
%       2016 May 29  sparse version         



%Cross-correlaiton
X= corr2norm(X);
Y = corr2norm(Y);
C = X'*Y;


%-------------------------
function Y = corr2norm(X);
%
% function Y = corr2norm(X);
%
% Given m x p data matrix X, perform centering and normalization operation on X.
%
% Chung, M.K., Hanson, J.L., Ye, J., Davidson, R.J. Pollak, S.D. 2015 
% Persistent Homology in Sparse Regression and Its Application to Brain Morphometry. 
% IEEE Transactions on Medical Imaging, 34:1928-1939
% http://www.stat.wisc.edu/~mchung/papers/chung.2015.TMI.pdf
%
% (C) Moo K. Chung
%  email://mkchung@wisc.edu
%  Department of Biostatisics and Medical Informatics
%  University of Wisconsin, Madison
%
%
% Update History: 
%       2015 Oct. 28 created
%       2016 May 29  sparse version         



%missing data treatment
%meanvol(isnan(meanvol))=0;
%meanvol(meanvol~=0)=1;


m= size(X,1);
p= size(X,2);

%[m p] =size(X);

meanX= nanmean(X,1); %mean without NaN
for i=1:p
    X(isnan(X(:,i)),i)=meanX(i); %replace missing with average
end

meanX=mean(X,1); %recompute mean

meanX=repmat(meanX,m,1);
X1=X-meanX;
diagX1 = sqrt(diag(X1'*X1));
X1=X1./repmat(diagX1', m,1);
Y=X1;




