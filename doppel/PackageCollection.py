from doppel.PackageAPI import PackageAPI
from typing import Dict
from typing import List


class PackageCollection:

    def __init__(self, packages):
        for pkg in packages:
            assert isinstance(pkg, PackageAPI)

        pkg_names = [pkg.name() for pkg in packages]
        if (len(set(pkg_names)) < len(packages)):
            msg = "All packages provided to PackageCollection must have unique names"
            raise ValueError(msg)

        self.pkgs = packages

    def package_names(self) -> List[str]:
        return([p.name() for p in self.pkgs])

    def all_classes(self) -> List[str]:
        """
        List of all classes that exist in at least
        one of the packages.
        """
        out = set([])
        for pkg in self.pkgs:
            out = out.union(pkg.class_names())
        return(list(out))

    def shared_classes(self) -> List[str]:
        """
        List of shared classes
        across all the packages in the collection
        """
        # Only work on shared classes
        out = set(self.pkgs[0].class_names())
        for pkg in self.pkgs[1:]:
            out = out.intersection(pkg.class_names())
        return(list(out))

    def non_shared_classes(self) -> List[str]:
        """
        List of all classes that are present in
        at least one but not ALL packages
        """
        all_classes = set(self.all_classes())
        shared_classes = set(self.shared_classes())
        return(list(all_classes.difference(shared_classes)))

    def all_functions(self) -> List[str]:
        """
        List of all functions that exist in at least
        one of the packages.
        """
        out = set([])
        for pkg in self.pkgs:
            out = out.union(pkg.function_names())
        return(list(out))

    def shared_functions(self) -> List[str]:
        """
        List of shared functions
        across all the packages in the collection
        """
        # Only work on shared classes
        out = set(self.pkgs[0].function_names())
        for pkg in self.pkgs[1:]:
            out = out.intersection(pkg.function_names())
        return(list(out))

    def non_shared_functions(self) -> List[str]:
        """
        List of all functions that are present in
        at least one but not ALL packages
        """
        all_funcs = set(self.all_functions())
        shared_funcs = set(self.shared_functions())
        return(list(all_funcs.difference(shared_funcs)))

    def shared_methods_by_class(self) -> Dict[str, List[str]]:
        """
        List of public methods in each shared
        class across all packages
        """
        out = {}
        shared_classes = self.shared_classes()
        for class_name in shared_classes:
            methods = set(self.pkgs[0].public_methods(class_name))
            for pkg in self.pkgs[1:]:
                methods = methods.intersection(pkg.public_methods(class_name))
            out[class_name] = list(methods)
        return(out)
