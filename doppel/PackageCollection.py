from doppel import PackageAPI
from typing import List


class PackageCollection:

    def __init__(self, packages):
        for pkg in packages:
            assert isinstance(pkg, PackageAPI)
        self.pkgs = packages

    def all_classes(self) -> List[str]:
        """
        List of all classes that exist in at least
        one of the packages.
        """
        out = set([])
        for pkg in self.pkgs:
            out = out.union(pkg.class_names())
        return(out)

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
        return(out)

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
