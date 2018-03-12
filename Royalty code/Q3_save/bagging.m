function [bags] = bagging(param, data_train)
    replacement = param.replacement;
    n = param.n;
    s = param.s;
    
    if replacement == 1
        %with replacement
        for i = 1:n
            randomIndex = randperm(size(data_train,1),round(s));
            bags{i} = data_train(randomIndex,:);
        end
    elseif replacement == 0
        %withoutreplacement
        t = round((size(data_train,1)-1)/n);
        randomIndexTemp = 1:size(data_train,1);
        for i = 1:n
            randomIndex = randperm(length(randomIndexTemp),t);
            bags{i} = data_train(randomIndex,:);
            randomIndexTemp(randomIndex) = [];
        end
    end
end