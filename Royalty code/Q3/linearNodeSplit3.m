function [childrenBest, infoGainBest] = linearNodeSplit3(param, rootNode, numfunct) % Compute the best "y=mx+p" split node for the bag

infoGainBest.x1 = 0;
infoGainBest.x2 = 0;
infoGainBest.Gain = 0;
childrenBest = [];
diff = 0;

%Linear Split Function y = m*x+p
for m = 1:numfunct
    while diff == 0
        randomDim = randi(param.dimensions,[1,2]);
        minYInt = min(rootNode(:,randomDim(1,2)));
        maxYInt = max(rootNode(:,randomDim(1,2)));
        if minYInt ~= maxYInt
            diff = 1;
        end
    end
    try
        randomSampYInt = randperm(round(abs(maxYInt - minYInt)/0.00001),numfunct);
    catch
        fnvjfn
    end
    
    %given a y intercept, calculate the gradients of the lines to the min
    %and max data points. These gradients are calculated for the 3
    %(numfunct) y intercepts which we try
    Grad1 = (randomSampYInt - min(rootNode(:,randomDim(1,2)))/0.00001)*0.00001./(-rootNode(rootNode(:,randomDim(1,2)) == min(rootNode(:,randomDim(1,2))),1));
    Grad2 = (randomSampYInt - max(rootNode(:,randomDim(1,2)))/0.00001)*0.00001./(-rootNode(rootNode(:,randomDim(1,2)) == max(rootNode(:,randomDim(1,2))),1));
    
    %for each yint, calculagte which gradient is larger
    if Grad1(m) > Grad2(m)
        maxGrad = Grad1(m);
        minGrad = Grad2(m);
    else
        maxGrad = Grad2(m);
        minGrad = Grad1(m);
    end
    % calculate a random gradient in between the min and max possible
    try
        randomSampGrad(m,:) = minGrad/0.00001 + randperm(round((maxGrad-minGrad)/0.00001),numfunct);
    catch
        hofgg
    end
    %perform linear split based on this y int and its gradient randomly
    %generated
    for p = 1:numfunct
        linSplitThreshold.x1 = randomSampGrad(m,p)*0.00001;
        linSplitThreshold.x2 = randomSampYInt(p)*0.00001;
        [children, infoGain] = childrenAndInfo3(param, rootNode, linSplitThreshold, randomDim);
        
        if infoGain > infoGainBest.Gain
            infoGainBest.x1 = randomSampGrad(m,p)*0.00001;
            infoGainBest.x2 = randomSampYInt(p)*0.00001;
            infoGainBest.Gain = infoGain;
            infoGainBest.dim = randomDim;
            childrenBest = children;
        end
    end
end
end
