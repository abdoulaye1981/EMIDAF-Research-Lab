from emidaf_core.kernel import Kernel
from emidaf_studio.app import app

kernel = Kernel()

kernel.start()

if __name__ == "__main__":

    app.run(debug=True)