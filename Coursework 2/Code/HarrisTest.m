im = imread('3.2_1.jpg');
im = im(:,:,1);
sigma = 1;

[dx,dy] = meshgrid(-1:1, -1:1);

Ix = conv2(double(im),dx, 'same');
Iy = conv2(double(im),dy, 'same');

dim = max(1,fix(6*sigma));
n = dim; m = dim;

[h1, h2] = meshgrid(-(m-1)/2:(m-1)/2, -(n-1)/2:(n-2)/2);
hg = exp(-(h1.^2+h2.^2)/(2*sigma^2));
[a,b] = size(hg);
sum = 0;

for i=1:a
    for j=1:b
        sum = sum + hg(i,j);
    end
end

g = hg ./ sum;

Ix2 = conv2(double(Ix.^2), g, 'same');
Iy2 = conv2(double(Iy.^2), g, 'same');
Ixy = conv2(double(Ix.*Iy), g, 'same');

R = (Ix2.*Iy2-Ixy.^2)./(Ix2+Iy2+eps);
