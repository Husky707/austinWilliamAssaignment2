import pymel.core as pmc
from  pymel.core.system import Path

class SceneFile(object):
    """Class used to to represent a DCC software scene file

    The class will be a convenient object that we can use to manipulate our 
    scene files. Examples features include the ability to predefine our naming 
    conventions and automatically increment our versions.

    Attributes:
        dir (Path, optional): Directory to the scene file. Defaults to ''.
        descriptor (str, optional): Short descriptor of the scene file. 
            Defaults to "main".
        version (int, optional): Version number. Defaults to 1.
        ext (str, optional): Extension. Defaults to "ma"

    """

    def __init__(self, dir = '', descriptor = 'main', version = 1, ext = 'ma'):
        """Initialises our attributes when class is instantiated.


        If the scene has not been saved, initialise the attributes based on 
        the defaults. Otherwise, if the scene is already saved, initialise 
        attributes based on the file name of the opened scene.

        """
        self._dir = Path(dir)
        self.descriptor = descriptor
        self.version = version
        self.ext = ext

        scene = pmc.system.sceneName()
        if scene:
            self.init_from_path(scene)

    @property
    def dir(self):
        return self._dir
    @dir.setter
    def dir(self, dPath):
        self._dir = Path(dPath)

    def init_from_path(self, openPath):
        self.dir = openPath.dirname()
        self.ext = openPath.ext[1:]
        splitName = openPath.name.split("_")
        self.descriptor = splitName[0]
        self.version = int(splitName[1].split(".")[0]) + 1

    def basename(self):

        name_pattern = "{descript}_{version}.{extention}"
        baseName = name_pattern.format(descript = self.descriptor, version = self.version, extention = self.ext)
        return baseName

    def path(self):

        return self.dir / self.basename()
        pass

    def save(self):
        """Saves the scene file."""

        try:
            pmc.system.saveAs(self.path())
        except:
            self.dir.makedirs_p()
            pmc.system.saveAs(self.path())

    def increment_and_save(self):
        self.version = self.get_next_version()
        self.save()

    def get_next_version(self):

        pattern = "{name}_*.{ext}".format(name = self.descriptor, ext = self.ext)
        versionList = []

        for eachFile in self.dir.files():
            if eachFile.fnmatch(pattern):
                versionList.append(int(self.parse_version(eachFile.name)))
        versionList = list(set(versionList))
        versionList.sort()
        return versionList[-1] + 1

    def parse_version(self, fileName):
        return fileName.split("_")[1].split(".")[0]