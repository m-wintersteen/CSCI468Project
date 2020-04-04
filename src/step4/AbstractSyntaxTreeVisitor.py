import collections
from antlr4 import *
from LittleParser import LittleParser
from LittleVisitor import LittleVisitor
from AbstractSyntaxTreeNode import AssignmentNode, IdentifierNode, LiteralNode, OperatorNode, WriteNode

class AbstractSyntaxTreeVisitor(LittleVisitor):

    # Visit a parse tree produced by LittleParser#program.
    def visitProgram(self, ctx:LittleParser.ProgramContext):
        self.tree = []
        self.visitChildren(ctx)
        for tree in self.tree:
            code = tree.generateCode()
            for line in code:
                print(line)
        return

    # SEMANTIC ACTIONS FOR AST

    # Visit a parse tree produced by LittleParser#assign_expr.
    def visitAssign_expr(self, ctx:LittleParser.Assign_exprContext):
        left = self.visit(ctx.id())
        right = self.visit(ctx.expr())
        node = AssignmentNode()
        node.left = left
        node.right = right
        self.tree.append(node)
        return


    # Visit a parse tree produced by LittleParser#id.
    def visitId(self, ctx:LittleParser.IdContext):
        return IdentifierNode(ctx.getText(), )


    # Visit a parse tree produced by LittleParser#expr.
    def visitExpr(self, ctx:LittleParser.ExprContext):
        addop = self.visit(ctx.expr_prefix())
        factor = self.visit(ctx.factor())
        if addop == None:
            return factor
        else:
            addop.right = factor
            return addop

    
    # Visit a parse tree produced by LittleParser#expr_prefix.
    def visitExpr_prefix(self, ctx:LittleParser.Expr_prefixContext):
        if ctx.expr_prefix() == None:
            return None
        expr_prefix = self.visit(ctx.expr_prefix())
        factor = self.visit(ctx.factor())
        addop = self.visit(ctx.addop())
        if expr_prefix == None:
            addop.left = factor
        else:
            expr_prefix.right = factor
            addop.left = expr_prefix
        return addop


    # Visit a parse tree produced by LittleParser#factor.
    def visitFactor(self, ctx:LittleParser.FactorContext):
        mulop = self.visit(ctx.factor_prefix())
        postfix_expr = self.visit(ctx.postfix_expr())
        if mulop == None:
            return postfix_expr
        else:
            mulop.right = postfix_expr
            return mulop


    # Visit a parse tree produced by LittleParser#addop.
    def visitAddop(self, ctx:LittleParser.AddopContext):
        return OperatorNode(ctx.getText())


    # Visit a parse tree produced by LittleParser#factor_prefix.
    def visitFactor_prefix(self, ctx:LittleParser.Factor_prefixContext):
        if ctx.factor_prefix() == None:
            return None
        factor_prefix = self.visit(ctx.factor_prefix())
        postfix_expr = self.visit(ctx.postfix_expr())
        mulop = self.visit(ctx.mulop())
        if factor_prefix == None:
            mulop.left = postfix_expr
        else:
            factor_prefix.right = postfix_expr
            mulop.left = factor_prefix
        return mulop


    # Visit a parse tree produced by LittleParser#postfix_expr.
    def visitPostfix_expr(self, ctx:LittleParser.Postfix_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LittleParser#mulop.
    def visitMulop(self, ctx:LittleParser.MulopContext):
        return OperatorNode(ctx.getText())


    # Visit a parse tree produced by LittleParser#primary.
    def visitPrimary(self, ctx:LittleParser.PrimaryContext):
        if ctx.expr() != None:
            return self.visit(ctx.expr())
        elif ctx.id() != None:
            return self.visit(ctx.id())
        else:
            return LiteralNode(ctx.getText())


    # Visit a parse tree produced by LittleParser#call_expr.
    def visitCall_expr(self, ctx:LittleParser.Call_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LittleParser#expr_list.
    def visitExpr_list(self, ctx:LittleParser.Expr_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LittleParser#expr_list_tail.
    def visitExpr_list_tail(self, ctx:LittleParser.Expr_list_tailContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LittleParser#write_stmt.
    def visitWrite_stmt(self, ctx:LittleParser.Write_stmtContext):
        ids = self.visit(ctx.id_list())
        for id in ids:
            write = WriteNode()
            write.left = id
            self.tree.append(write)
        return


    # Visit a parse tree produced by LittleParser#id_list.
    def visitId_list(self, ctx:LittleParser.Id_listContext):
        id = self.visit(ctx.id())
        tail = self.visit(ctx.id_tail())
        return [id, *tail]


    # Visit a parse tree produced by LittleParser#id_tail.
    def visitId_tail(self, ctx:LittleParser.Id_tailContext):
        if ctx.id() == None:
            return []
        id = self.visit(ctx.id())
        tail = self.visit(ctx.id_tail())
        return [id, *tail]


    # Visit a parse tree produced by LittleParser#str.
    def visitStr(self, ctx:LittleParser.StrContext):
        return LiteralNode(ctx.getText())



    # AST UTILITY FUNCTIONS
    def printTree(self, node):
        print('Node[label:{},text:{}]'.format(node.label, node.text))
        if node.left != None:
            self.printTree(node.left)
        if node.right != None:
            self.printTree(node.right)