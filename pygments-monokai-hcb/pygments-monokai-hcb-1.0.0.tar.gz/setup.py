"""
   Copyright (C) 2016 HandcraftedBits

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

from distutils.core import setup

setup(
    name="pygments-monokai-hcb",
    packages=["monokai_hcb"],
    version="1.0.0",
    description="Customized HandcraftedBits Monokai style for Pygments",
    author="HandcraftedBits",
    author_email="opensource@handcraftedbits.com",
    url="https://github.com/handcraftedbits/pygments-style-monokai-hcb",
    download_url="https://github.com/handcraftedbits/pygments-style-monokai-hcb/tarball/1.0.0",
    keywords=["pygments"],
    classifiers=[],

    entry_points="""
        [pygments.styles]
        monokai-hcb=monokai_hcb.style:MonokaiHcbStyle
    """,
)
