from dataclasses import dataclass
import math
import copy
pi = math.pi
@dataclass(frozen = True)
class GlobeRect:
    lLat: float
    uLat: float
    wLong: float
    eLong: float
@dataclass(frozen = True)
class Region:
    rect: GlobeRect
    terrain: str
@dataclass(frozen=True)
class RegionCondition:
    region: Region
    year: int
    population: int
    emissions: float

def emissions_per_capita(a: RegionCondition):
    return a.emissions/a.population
def region_area(a: GlobeRect):
    width = abs((a.eLong - a.wLong))/360.0
    llat = a.lLat
    ulat = a.uLat
    r = 6371.0
    bigcap = 0
    smallcap = 0
    hemiArea = pi*2.0*(r**2)
    if llat <= 0:
        bigcap = 2*hemiArea - (1-math.sin(math.radians(abs(llat))))
    else:
        bigcap = 2.0*pi*(r**2) - 2.0*pi*(r**2)*(1-math.sin(math.radians(abs(llat))))
    if ulat <= 0:
        smallcap = 2*hemiArea - (1-math.sin(math.radians(abs(ulat))))
    else:
        smallcap = 2.0*pi*(r**2)*(1-math.sin(math.radians(ulat)))
    return (width)*(bigcap - smallcap)
def emissions_per_square_km(a: RegionCondition):
    return emissions_per_capita(a)*a.population/(region_area(a.region.rect))
def densest(regions: list):
    density = []
    for i in range(len(regions)):
        print("i: ", i, ", density: ", (regions[i].population)/(region_area(regions[i].region.rect)))
        density.append((regions[i].population)/(region_area(regions[i].region.rect)))
    return regions[(density.index(max(density)))]
def project_condition(a: RegionCondition, years: int):
    rates = {"mountains": 1.0005, "ocean": 1.00001, "forest": 0.99999, "other": 1.00003}
    newPop = int(a.population*(rates.get(a.region.terrain)**years))
    b = RegionCondition(a.region, a.year + years, newPop, a.emissions)
    return b
SLO =  RegionCondition(Region(GlobeRect(34, 36, 122, 120), "ocean"), 2006, 260498, 800000)
Bakersfield =  RegionCondition(Region(GlobeRect(34.4, 35.9, 120.2, 118.2), "other"), 2023, 407615, 1000000)
Humboldt =  RegionCondition(Region(GlobeRect(40, 41, 125, 124), "ocean"), 2023, 136310, 500000)
LA = RegionCondition(Region(GlobeRect(34, 35, 119, 118), "other"), 2023, 3849000, 345800000)
example_regions = [SLO, Bakersfield, Humboldt, LA]