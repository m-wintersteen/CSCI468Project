import collections
from antlr4 import *
from LittleParser import LittleParser
from LittleVisitor import LittleVisitor
from AbstractSyntaxTreeNode import AssignmentNode, IdentifierNode, LiteralNode, OperatorNode, ReadNode, WriteNode
from Translator import Translator

class AbstractSyntaxTreeVisitor(LittleVisitor):

    # Visit a parse tree produced by LittleParser#program.
    def visitProgram(self, ctx:LittleParser.ProgramContext):
        # setup symbol table
        self.error = None
        self.symbolTable = collections.deque()
        self.enterScope()
        # setup abstract syntax tree
        self.tree = []
        # traverse parse tree
        self.visitChildren(ctx)
        ir = []
        for tree in self.tree:
            ir = ir + tree.generateCode()
        for line in ir:
            print(';' + line)
        translator = Translator()
        tiny = translator.translate(ir, self.symbolTable[0])
        for line in tiny:
            print(line)
        self.exitScope()
        return


    # SEMANTIC ACTIONS FOR AST

    # Visit a parse tree produced by LittleParser#assign_expr.
    def visitAssign_expr(self, ctx:LittleParser.Assign_exprContext):
        id = self.visit(ctx.id())
        symbol = self.getSymbol(id)
        left = IdentifierNode(id, symbol['type'])
        right = self.visit(ctx.expr())
        node = AssignmentNode()
        node.left = left
        node.right = right
        self.tree.append(node)
        return


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
        if ctx.primary() != None:
            return self.visit(ctx.primary())
        else:
            return self.visit(ctx.call_expr())


    # Visit a parse tree produced by LittleParser#primary.
    def visitPrimary(self, ctx:LittleParser.PrimaryContext):
        if ctx.expr() != None:
            return self.visit(ctx.expr())
        elif ctx.id() != None:
            id = self.visit(ctx.id())
            symbol = self.getSymbol(id)
            return IdentifierNode(id, symbol['type'])
        else:
            val = ctx.getText()
            type = 'FLOAT' if '.' in val else 'INT'
            return LiteralNode(val, type)


    # Visit a parse tree produced by LittleParser#call_expr.
    def visitCall_expr(self, ctx:LittleParser.Call_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LittleParser#expr_list.
    def visitExpr_list(self, ctx:LittleParser.Expr_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LittleParser#expr_list_tail.
    def visitExpr_list_tail(self, ctx:LittleParser.Expr_list_tailContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LittleParser#addop.
    def visitAddop(self, ctx:LittleParser.AddopContext):
        return OperatorNode(ctx.getText())


    # Visit a parse tree produced by LittleParser#mulop.
    def visitMulop(self, ctx:LittleParser.MulopContext):
        return OperatorNode(ctx.getText())


    # Visit a parse tree produced by LittleParser#write_stmt.
    def visitWrite_stmt(self, ctx:LittleParser.Write_stmtContext):
        ids = self.visit(ctx.id_list())
        for id in ids:
            type = self.getSymbol(id)['type']
            write = WriteNode()
            write.left = IdentifierNode(id, type)
            self.tree.append(write)
        return

    
    # Visit a parse tree produced by LittleParser#read_stmt.
    def visitRead_stmt(self, ctx:LittleParser.Read_stmtContext):
        ids = self.visit(ctx.id_list())
        for id in ids:
            type = self.getSymbol(id)['type']
            read = ReadNode()
            read.left = IdentifierNode(id, type)
            self.tree.append(read)
        return


    # SEMANTIC ACTIONS FOR SYMBOL TABLE

    # Visit a parse tree produced by LittleParser#string_decl.
    def visitString_decl(self, ctx:LittleParser.String_declContext):
        id = self.visit(ctx.id())
        val = self.visit(ctx.str())
        self.addSymbol(id, 'STRING', val)
        return


    # Visit a parse tree produced by LittleParser#var_decl.
    def visitVar_decl(self, ctx:LittleParser.Var_declContext):
        typ = self.visit(ctx.var_type())
        ids = self.visit(ctx.id_list())
        for id in ids:
            self.addSymbol(id, typ)
        return


    # Visit a parse tree produced by LittleParser#func_decl.
    def visitFunc_decl(self, ctx:LittleParser.Func_declContext):
        self.enterScope()
        id = self.visit(ctx.id())
        decls = self.visit(ctx.param_decl_list())
        for (id, typ) in decls:
            self.addSymbol(id, typ)
        self.visit(ctx.func_body())
        self.exitScope()
        return


    # Visit a parse tree produced by LittleParser#param_decl_list.
    def visitParam_decl_list(self, ctx:LittleParser.Param_decl_listContext):
        if ctx.param_decl() == None:
            return []
        decl = self.visit(ctx.param_decl())
        return [decl, *self.visit(ctx.param_decl_tail())]


    # Visit a parse tree produced by LittleParser#param_decl.
    def visitParam_decl(self, ctx:LittleParser.Param_declContext):
        typ = self.visit(ctx.var_type())
        id = self.visit(ctx.id())
        return (id, typ)


    # Visit a parse tree produced by LittleParser#param_decl_tail.
    def visitParam_decl_tail(self, ctx:LittleParser.Param_decl_tailContext):
        if ctx.param_decl() == None:
            return []
        decl = self.visit(ctx.param_decl())
        return [decl, *self.visit(ctx.param_decl_tail())]
    

    # Visit a parse tree produced by LittleParser#if_stmt.
    def visitIf_stmt(self, ctx:LittleParser.If_stmtContext):
        self.enterScope()
        self.visitChildren(ctx)
        self.exitScope()
        return


    # Visit a parse tree produced by LittleParser#else_part.
    def visitElse_part(self, ctx:LittleParser.Else_partContext):
        if ctx.decl() == None:
            return
        self.enterScope()
        self.visitChildren(ctx)
        self.exitScope()
        return


    # Visit a parse tree produced by LittleParser#while_stmt.
    def visitWhile_stmt(self, ctx:LittleParser.While_stmtContext):
        self.enterScope()
        self.visitChildren(ctx)
        self.exitScope()
        return


    # RETURN TOKEN TEXT OR LIST OF TOKEN TEXT

    # Visit a parse tree produced by LittleParser#var_type.
    def visitVar_type(self, ctx:LittleParser.Var_typeContext):
        return ctx.getText()


    # Visit a parse tree produced by LittleParser#id.
    def visitId(self, ctx:LittleParser.IdContext):
        return ctx.getText()


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
        return ctx.getText()

    
     # UTILITY FUNCTIONS FOR SYMBOL TABLES

    # enter a new scope
    def enterScope(self):
        self.symbolTable.appendleft(collections.OrderedDict())


    # leave the current scope
    def exitScope(self):
        self.symbolTable.popleft()


    # add a symbol to the table for the current scope
    def addSymbol(self, id, type, val=None):
        if not id in self.symbolTable[0]:
            self.symbolTable[0][id] = {'value':val,'type':type}
        else:
            if not self.error:
                self.error = id


    # lookup a symbol in the current scope and parent scopes
    def getSymbol(self, id):
        for symbolTable in self.symbolTable:
            if id in symbolTable:
                return symbolTable[id]
        return None