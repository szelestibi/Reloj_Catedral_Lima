--[[ peso y balance agujas catedral de lima ]]

--[[ 10 cm de fierro        = 260 gr
     10 cm de aluminio      =  24 gr
     aguja de minutos       = 700 gr
     aguja de horas         = 600 gr
     longitud aguja minutos =  94 cm
     longitud aguja horas   =  71 cm ]]

pesoAl  =  2.4;                        -- peso del perfil de aluminio [gr/cml]
pesoFe  = 26.0;                        -- peso de la varra de fierro  [gr/cml]

pesoMin = 700;                         -- peso de la aguja de plastico de minutos
pesoHor = 600;                         -- peso de la aguja de plastico de horas

rxMin   = 41;                          -- centro de peso del minutero de plastico
rxHor   = 36;                          -- centro de peso de la aguja de plastico horaria

minMomentum = pesoMin * rxMin;         -- momento del minutero de plastico
horMomentum = pesoHor * rxHor;         -- momento del horario de plastico

function calcMom(ll,lr,mat)            -- calcular momento de un brazo con eje: left side length, right side length, material [gr/cm]
 return((lr+ll)/2 * mat * (lr-ll))
end

function balance(bMom,ls,mtr)          -- calcular dimesion del brazo para balanzar otro brazo: moment, left side length, material
 for adl=1,100 do
  actMom = calcMom(ls,ls+adl,mtr)
--print('right: '..ls + adl..' cm, actMom: '..actMom..', bMom: '..bMom..', diff: '..(bMom-actMom))
  if((bMom-actMom) < 0) then return(ls+adl-1) end
 end
end

print('')
print('aguja de minutos de plastico, momento: '..minMomentum..' gr x cm')
print('aguja de minutos de plastico, contrapeso de fierro: '..balance(minMomentum,10,pesoFe)..' cm')
print()
print('aguja de horas de plastico, momento: '..horMomentum..' gr x cm')
print('aguja de horas de plastico, contrapeso de fierro: '..balance(horMomentum,10,pesoFe)..' cm')
print()
