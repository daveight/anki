# Copyright: Daveight and contributors
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
"""
C++ implementation of the Type Mapper API
"""

from testing.framework.string_utils import render_template
from testing.framework.type_mapper import TypeMapper
from testing.framework.syntax.syntax_tree import SyntaxTree


class CppTypeMapper(TypeMapper):
    """
    C++ type mapper.
    """

    def visit_array(self, node: SyntaxTree, context):
        """
        C++ mapping for array-type

        :param node: target syntax tree node
        :param context: generation context
        :return: C++ array-type declaration
        """
        return self.visit_list(node, context)

    def visit_list(self, node: SyntaxTree, context):
        """
        C++ mapping for list-type

        :param node: target syntax tree node
        :param context: generation context
        :return: C++ list-type declaration
        """
        return 'vector<' + self.render(node.first_child(), context) + '>'

    def visit_map(self, node: SyntaxTree, context):
        """
        C++ mapping for map-type

        :param node: target syntax tree node
        :param context: generation context
        :return: C++ map-type declaration
        """
        converters = [self.render(child, context) for child in node.nodes]
        return 'map<' + converters[0] + ', ' + converters[1] + '>'

    def visit_int(self, node: SyntaxTree, context):
        """
        C++ mapping for int-type

        :param node: target syntax tree node
        :param context: generation context
        :return: C++ int-type declaration
        """
        return 'int'

    def visit_long(self, node: SyntaxTree, context):
        """
        C++ mapping for long-type

        :param node: target syntax tree node
        :param context: generation context
        :return: C++ long-type declaration
        """
        return 'long int'

    def visit_float(self, node: SyntaxTree, context):
        """
        C++ mapping for float-type

        :param node: target syntax tree node
        :param context: generation context
        :return: C++ float-type declaration
        """
        return 'double'

    def visit_string(self, node: SyntaxTree, context):
        """
        C++ mapping for string-type

        :param node: target syntax tree node
        :param context: generation context
        :return: C++ string-type declaration
        """
        return 'string'

    def visit_bool(self, node: SyntaxTree, context):
        """
        C++ mapping for string-type

        :param node: target syntax tree node
        :param context: generation context
        :return: C++ string-type declaration
        """
        return 'bool'
 
    def visit_obj(self, node: SyntaxTree, context):
        """
        C++ mapping for object-type. Stores type definition to the context

        :param node: target syntax tree node
        :param context: generation context
        :return: C++ object-type declaration
        """
        type_name = node.node_type
        props, _ = self.get_args(node, context)
        typedef = render_template(''' 
            struct {{type_name}} {
                {% for prop in props %}\t{{prop.type}} {{prop.name}};\n{% endfor %}};
            ''', type_name=type_name, props=props)
        context[type_name] = typedef
        return type_name

    def visit_void(self, node: SyntaxTree, context):
        """
        C++ mapping for void-type.
        :param node: target syntax tree node
        :param context: generation context
        :return: C++ void-type declaration
        """
        return 'void'