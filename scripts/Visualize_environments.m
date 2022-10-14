clear

create_plot('uc1-LeestUrban', 'UC1_100CPE_UrbanVillage');
create_plot('uc2-LeestRural', 'UC2_50CPE_Rural');
create_plot('uc3-Ghent', 'UC3_300CPE_UrbanCity');

function create_plot(env, simName)

simNumber           = 0;
inputFolder         = '../data/environments/';
outputFolderA       = '../data/';
outputFolder        = strcat(outputFolderA,simName);       

areaSHPfile         = shaperead(strcat(inputFolder,env,'/CoverArea.shp'));
buildingsSHPfile    = shaperead(strcat(inputFolder,env,'/Buildings.shp'));
roadSHPfile         = shaperead(strcat(inputFolder,env,'/Roads.shp'));
infoArea            = shapeinfo(strcat(inputFolder,env,'/CoverArea.shp'));

BSfilename          = strcat(outputFolder,'/basestations_',num2str(simNumber),'.csv');
BSopt = detectImportOptions(BSfilename);
BS = readtable(BSfilename,BSopt);
BSSize = size(BS,1);

% Creation of the Connected and unconnected base station (POP) matrix
p=1;
q=1;
cPOP = false;
ucPOP = false;
for i=1:BSSize
    if (strcmpi(BS.BSType(i),'POP'))
        if (strcmpi(BS.is_active(i),'TRUE'))
              ConnectedPOP(p,:) = BS(i,:); % List of PoP active
              cPOP = true;
              p=p+1;
        else 
              UnconnectedPOP(q,:) = BS(i,:); % List of PoP inactive
              ucPOP = true;
              q=q+1;
        end
    end
end

% Creation of the Connected and unconnected base station (EDGE) matrix
a=1;
b=1;
cBS = false;
ucBS = false;
for i=1:BSSize
    if (strcmpi(BS.BSType(i),'EDGE'))
        if (strcmpi(BS.is_active(i),'TRUE'))
              ConnectedBS(a,:) = BS(i,:);  %  list of Bs that are active due connected users
              cBS = true;
              a=a+1;
        else 
              UnconnectedBS(b,:) = BS(i,:); % list fo BS that are disavtive due connected users
              ucBS = true;
              b=b+1;
        end
    end
end

ConnectedBSSize = 0;
if (cPOP==true) 
    ConnectedPOPSize = size(ConnectedPOP,1);
end
% Creation of the mesh link for BS (edge)
a=1;
b=1;
l=1;
m=1;
n=1;

for i=1:BSSize
      if (strcmpi(BS.is_active(i),'TRUE'))
          meshBS = split(BS.RoutetoPoP(i),"-");
          meshBSSize = size(meshBS,1);
          if (meshBSSize>2)
              EDGE = meshBS(meshBSSize-2,1);
              bsid = 1 + str2double(cellstr(meshBS(meshBSSize-2)));
              %bsid = 1+EDGE;
              if (strcmpi(BS.is_active(bsid),'TRUE'))
                  if (strcmpi(BS.BSType(i),'POP') || strcmpi(BS.BSType(bsid),'POP'))
                    ConnectedPOPlink(l,1)= BS.x_m_(i);   
                    ConnectedPOPlink(l,2)= BS.y_m_(i);
                    ConnectedPOPlink(l,3)= BS.x_m_(bsid);
                    ConnectedPOPlink(l,4)= BS.y_m_(bsid);
                    l=l+1;
                  else
                    MeshClink(m,1)= BS.x_m_(i);   
                    MeshClink(m,2)= BS.y_m_(i);
                    MeshClink(m,3)= BS.x_m_(bsid);
                    MeshClink(m,4)= BS.y_m_(bsid);
                    m=m+1;
                  end
              else
                  MeshUClink(n,1)= BS.x_m_(i);   
                  MeshUClink(n,2)= BS.y_m_(i);
                  MeshUClink(n,3)= BS.x_m_(bsid);
                  MeshUClink(n,4)= BS.y_m_(bsid);
                  n=n+1;
              end
          end
          
          for j=1:(meshBSSize-1)
              
              
          end
      else
          meshBS = split(BS.RoutetoPoP(i),"-");
          meshBSSize = size(meshBS,1);
          for j=1:(meshBSSize-1)
              bsid = 1 + str2double(cellstr(meshBS(j)));
              MeshUClink(n,1)= BS.x_m_(i);   
              MeshUClink(n,2)= BS.y_m_(i);
              MeshUClink(n,3)= BS.x_m_(bsid);
              MeshUClink(n,4)= BS.y_m_(bsid);
              n=n+1;
          end
      end
end

% Figure initialization
figA = figure('Color','w','Position',[25 25 1000 650]); %[left bottom width height]
axesA = axes('Parent',figA);
Xmin = infoArea.BoundingBox(1,1);
Xmax = infoArea.BoundingBox(2,1);
Ymin = infoArea.BoundingBox(1,2);
Ymax = infoArea.BoundingBox(2,2);
axesA.XLim = [Xmin Xmax];
axesA.YLim = [Ymin Ymax];
hold(axesA,'on');
mapshow(areaSHPfile);
mapshow(buildingsSHPfile, 'FaceColor', [0.8 0.8 0.8], 'EdgeColor', [0.5 0.5 0.5]);
mapshow(roadSHPfile,'LineStyle',':', 'Color', [0.5 0.5 0.5],'LineWidth',2);

% Connected POPs
if (cPOP==true) 
    scatterPOPa = scatter(ConnectedPOP.x_m_,ConnectedPOP.y_m_,75,'s','MarkerEdgeColor','g','MarkerFaceColor','g');
    set(scatterPOPa,'DisplayName','PoP Nodes Connected');
else
    scatterPOPa = scatter(0,0,'s','g');
    set(scatterPOPa,'DisplayName','PoP Nodes Connected');
end

% Unconnected POP
if (ucPOP==true) 
    scatterPOPb = scatter(UnconnectedPOP.x_m_,UnconnectedPOP.y_m_,75,'s','MarkerEdgeColor','g','MarkerFaceColor',[1 1 1]);
    set(scatterPOPb,'DisplayName','PoP Nodes Unconnected');
else
    scatterPOPb = scatter(0,0,'s','MarkerEdgeColor','g','MarkerFaceColor',[1 1 1]);
    set(scatterPOPb,'DisplayName','PoP Nodes Unconnected');
end

% Connected EDGEs
if(ConnectedBSSize > 0)
    scatterA = scatter(ConnectedBS.x_m_,ConnectedBS.y_m_,75,'^','r','filled');
    set(scatterA,'DisplayName','Edge Nodes Connected ');
end

% Unconnected EDGEs
if (ucBS== true)
    scatterB = scatter(UnconnectedBS.x_m_,UnconnectedBS.y_m_,75,'Marker','^','MarkerEdgeColor','r');
    set(scatterB,'DisplayName','Edge Nodes Unconnected');
else 
    scatterB = scatter(0,0,'^','MarkerEdgeColor','r');
    set(scatterB,'DisplayName','Edge Nodes Unconnected');
end


end