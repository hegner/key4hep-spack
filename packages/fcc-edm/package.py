
from spack.pkg.k4.key4hep_stack import Key4hepPackage 

class FccEdm(CMakePackage, Key4hepPackage):
    """Event data model of FCC"""

    homepage = "https://github.com/HEP-FCC/fcc-edm"
    url      = "https://github.com/HEP-FCC/fcc-edm/archive/v0.5.5.tar.gz"
    git =      "https://github.com/HEP-FCC/fcc-edm.git"

    version('master', branch='master')
    version('0.5.8', sha256='a5a5456d601890e58f8b876e39c526629e92ae1f44b18a502774691059343d78')
    version('0.5.7', sha256='8fe7f45014a401d635c00bad12c8fd251e2cabbabdfea0304c06c3ac926c60ca')
    version('0.5.6', sha256='aaf4ff58dfbdf9dfc3f755ad8b14d5e5701ed875f4031b1f7538deaf0f027705')
    version('0.5.5', sha256='a07a2f1304ce08a6d9819200c77e4a739f1e96f2ebb59715ebc27992e6a014e0')
    version('0.5.4', '236206ca4e00f239d574bfcd6aa44b53')
    version('0.5.3', 'ce4e041c795a22e7a6b4558ebe5a9545')
    version('0.5.2', '8f17139fae2bbc14fca88843791be9c3')

    patch('cpack.patch', when="@:0.5.6")

    depends_on('cmake', type='build')
    depends_on('python', type='build')
    depends_on('dag', when="@:0.5.6")
    depends_on('root@6.08:')
    depends_on('podio@:0.9.2', when='@:0.5.5')
    depends_on('podio@0.10.0:', when='@0.5.6')
    depends_on('podio@0.12.0:', when='@0.5.7:')

    # Make podio build dependencies explicit until we make podio bring them
    # along properly
    depends_on('py-jinja2@2.10.1:', type='build')
    depends_on('py-pyyaml', type='build')

    def cmake_args(self):
        args = []
        # C++ Standard
        args.append('-DCMAKE_CXX_STANDARD=17')
        return args

    # Override pre-defined test step
    # Multiple tests access to the same root file, thus we avoid parallel
    # execution at this stage
    def check(self):
        with working_dir(self.build_directory):
            make("test", "CTEST_OUTPUT_ON_FAIL=1")

    def setup_dependent_build_environment(self, env, dependent_spec):
            env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)

    def setup_run_environment(self, env):
            env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)
