from vtk import vtkActor
from vtk import vtkPolyDataMapper
from vtk import vtkConeSource, vtkCubeSource, vtkParametricEllipsoid, vtkParametricFunctionSource, vtkParametricTorus


class VTKSpecificActor:
    def __init__(self, geometry: str, dimensions, **kwargs):
        """
        geometry: string of what to draw
            available options: "cone", "rectprism", "ellipsoid", "torus"
        dimensions: dimensions of the bounding box. ideally a tuple with three
            arguments
        """
        self.geometry = geometry
        self.kwargs = kwargs

        if len(dimensions) == 3:
            self.dim = dimensions
        elif len(dimensions) == 2: # x and y dimensions are same/square base box
            self.dim[0] = dimensions[0]
            self.dim[1] = dimensions[0]
            self.dim[2] = dimensions[1]
        elif len(dimensions) == 1:
            self.dim = [dimensions for _ in range(3)]  # creates a cube bounding box
        else:
            raise ValueError("Bounding box has " + str(len(dimensions)) + " dimensions?")

        # all of the generate functions technically do run at every class instance
        # but the non-matching geometries generate empty actors
        _command_dict = {
            "cone": self._generate_cone(),
            "rectprism": self._generate_rectprism(),
            "ellipsoid": self._generate_ellipsoid(),
            "torus": self._generate_torus()
        }

        self.actor = _command_dict[geometry]

    def _other_vtk_settings(self):
        self._mapper = vtkPolyDataMapper()

    def _generate_cone(self):
        if self.geometry != "cone":
            return vtkActor()
        else:
            _actor = vtkActor()
            self._other_vtk_settings()

            _source = vtkConeSource()
            _source.SetHeight(self.dim[2])
            _source.SetRadius(self.dim[0] / 2)

            if 'resolution' in self.kwargs:
                _source.SetResolution(self.kwargs['resolution'])
            elif 'center' in self.kwargs:
                _source.SetCenter(self.kwargs['center'])
            elif 'direction' in self.kwargs:
                _source.SetDirection(self.kwargs['direction'])

            self._mapper.SetInputConnection(_source.GetOutputPort())
            _actor.SetMapper(self._mapper)

            return _actor

    def _generate_rectprism(self):
        if self.geometry != "rectprism":
            return vtkActor()
        else:
            _actor = vtkActor()
            self._other_vtk_settings()

            _source = vtkCubeSource()
            _source.SetXLength(self.dim[0])
            _source.SetYLength(self.dim[1])
            _source.SetZLength(self.dim[2])
            _source.Update()

            if 'center' in self.kwargs:
                _source.SetCenter(self.kwargs['center'])

            self._mapper.SetInputConnection(_source.GetOutputPort())
            _actor.SetMapper(self._mapper)

            return _actor

    def _generate_ellipsoid(self):
        if self.geometry != "ellipsoid":
            return vtkActor()
        else:
            _actor = vtkActor()
            self._other_vtk_settings()

            _param_ellipsoid = vtkParametricEllipsoid()
            _param_ellipsoid.SetXRadius(self.dim[0]/2)
            _param_ellipsoid.SetYRadius(self.dim[1]/2)
            _param_ellipsoid.SetZRadius(self.dim[2]/2)

            _source = vtkParametricFunctionSource()
            _source.SetParametricFunction(_param_ellipsoid)

            if 'center' in self.kwargs:
                _source.SetCenter(self.kwargs['center'])
            elif 'resolution' in self.kwargs:
                _source.SetUResolution(self.kwargs['resolution'])
                _source.SetVResolution(self.kwargs['resolution'])

            self._mapper.SetInputConnection(_source.GetOutputPort())
            _actor.SetMapper(self._mapper)

            return _actor

    def _generate_torus(self):
        if self.geometry != "torus":
            return vtkActor()
        else:
            _actor = vtkActor()
            self._other_vtk_settings()

            _param_torus = vtkParametricTorus()
            _param_torus.SetRingRadius(self.dim[0] / 2)
            _param_torus.SetCrossSectionRadius(self.dim[2] / 2)

            _source = vtkParametricFunctionSource()
            _source.SetParametricFunction(_param_torus)

            if 'center' in self.kwargs:
                _source.SetCenter(self.kwargs['resolution'])
            elif 'resolution' in self.kwargs:
                _source.SetUResolution(self.kwargs['resolution'])
                _source.SetVResolution(self.kwargs['resolution'])

            self._mapper.SetInputConnection(_source.GetOutputPort())
            _actor.SetMapper(self._mapper)
            return _actor
