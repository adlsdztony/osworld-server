import tempfile
import unittest
from pathlib import Path

from src.server import app


class RunBashScriptTest(unittest.TestCase):
    def test_executes_script_and_returns_output(self) -> None:
        with tempfile.TemporaryDirectory() as working_dir:
            marker = Path(working_dir) / "marker.txt"
            script = f"printf osworld-server-ok | tee {marker.name}"

            with app.test_client() as client:
                response = client.post(
                    "/run_bash_script",
                    json={"script": script, "working_dir": working_dir},
                )

            self.assertEqual(response.status_code, 200, response.get_json())
            self.assertEqual(
                response.get_json(),
                {
                    "status": "success",
                    "output": "osworld-server-ok",
                    "error": "",
                    "returncode": 0,
                },
            )
            self.assertEqual(marker.read_text(), "osworld-server-ok")


if __name__ == "__main__":
    unittest.main()
