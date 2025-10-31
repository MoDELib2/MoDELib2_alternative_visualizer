# MoDELib2


# Notes
## Modification on source code

### gcc15 on linux
- code won't compile without "#include <cassert>". It had to be added on the following list of files.

```
  include/Geometry/PlaneLineIntersection.h:#include <cassert>
  include/Geometry/SweepPlane.h:#include <cassert>
  src/DislocationDynamicsBase/DislocationFieldBase.cpp:#include <cassert>
  src/Geometry/Plane.cpp:#include <cassert>
  src/Geometry/LineSimplexIntersection.cpp:#include <cassert>
  src/Geometry/PlanePlaneIntersection.cpp:#include <cassert>
  src/Geometry/PlaneSegmentIntersection.cpp:#include <cassert>
  src/Lattices/LatticeDirection.cpp:#include <cassert>
  src/Lattices/LatticeLine.cpp:#include <cassert>
  src/Lattices/LatticeVector.cpp:#include <cassert>
  src/Lattices/RLLL.cpp:#include <cassert>
  src/Lattices/LLL.cpp:#include <cassert>
  src/Lattices/RationalLatticeDirection.cpp:#include <cassert>
  src/Lattices/ReciprocalLatticeVector.cpp:#include <cassert>
  src/Mesh/BarycentricTraits.cpp:#include <cassert>
```


### pyMoDELib
- Matthew added python API that extracts segment information


### tests/mpl_visualize_dislocation
- Added visualization code to plot dislocation segments on each glide plane using matplotlib.
- (?) We need to find a way to plot the segments on the actual glide plane size
