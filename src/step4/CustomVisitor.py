import collections
from antlr4 import *
from LittleParser import LittleParser
from LittleVisitor import LittleVisitor

class CustomVisitor(LittleVisitor):

    # Visit a parse tree produced by LittleParser#program.
    def visitProgram(self, ctx:LittleParser.ProgramContext):
        # initialization step
        self.error = None
        self.symbolTable = collections.OrderedDict()
        self.scope = []
        self.block = 0
        self.addScope('GLOBAL')
        # visit children
        self.visitChildren(ctx)
        # finalization step
        if self.error:
            print('DECLARATION ERROR {}'.format(self.error))
        else:
            for scope, table in self.symbolTable.items():
                print('Symbol table {}'.format(scope))
                for var, attr in table.items():
                    if (attr['value']):
                        print('name {} type {} value {}'.format(var, attr['type'], attr['value']))
                    else:
                        print('name {} type {}'.format(var, attr['type']))
                print()
        return


    # Visit a parse tree produced by LittleParser#string_decl.
    def visitString_decl(self, ctx:LittleParser.String_declContext):
        id = self.visit(ctx.id())
        val = self.visit(ctx.str())
        self.addSymbol(id, 'STRING', val)
        return


    # Visit a parse tree produced by LittleParser#id.
    def visitId(self, ctx:LittleParser.IdContext):
        return ctx.getText()


    # Visit a parse tree produced by LittleParser#str.
    def visitStr(self, ctx:LittleParser.StrContext):
        return ctx.getText()


    # Visit a parse tree produced by LittleParser#var_decl.
    def visitVar_decl(self, ctx:LittleParser.Var_declContext):
        typ = self.visit(ctx.var_type())
        ids = self.visit(ctx.id_list())
        for id in ids:
            self.addSymbol(id, typ)
        return


    # Visit a parse tree produced by LittleParser#var_type.
    def visitVar_type(self, ctx:LittleParser.Var_typeContext):
        return ctx.getText()


    # Visit a parse tree produced by LittleParser#id_list.
    def visitId_list(self, ctx:LittleParser.Id_listContext):
        id = self.visit(ctx.id())
        return [id, *self.visit(ctx.id_tail())]


    # Visit a parse tree produced by LittleParser#id_tail.
    def visitId_tail(self, ctx:LittleParser.Id_tailContext):
        if ctx.id() == None:
            return []
        id = self.visit(ctx.id())
        return [id, *self.visit(ctx.id_tail())]


    # Visit a parse tree produced by LittleParser#func_decl.
    def visitFunc_decl(self, ctx:LittleParser.Func_declContext):
        id = self.visit(ctx.id())
        self.addScope(id)
        decls = self.visit(ctx.param_decl_list())
        for (id, typ) in decls:
            self.addSymbol(id, typ)
        self.visit(ctx.func_body())
        self.scope.pop()
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
        self.block = self.block + 1
        self.addScope('BLOCK {}'.format(self.block))
        self.visitChildren(ctx)
        self.scope.pop()
        return


    # Visit a parse tree produced by LittleParser#else_part.
    def visitElse_part(self, ctx:LittleParser.Else_partContext):
        if ctx.decl() == None:
            return
        self.block = self.block + 1
        self.addScope('BLOCK {}'.format(self.block))
        self.visitChildren(ctx)
        self.scope.pop()
        return


    # Visit a parse tree produced by LittleParser#while_stmt.
    def visitWhile_stmt(self, ctx:LittleParser.While_stmtContext):
        self.block = self.block + 1
        self.addScope('BLOCK {}'.format(self.block))
        self.visitChildren(ctx)
        self.scope.pop()
        return
    

    # UTILITY FUNCTIONS FOR SYMBOL TABLES

    def addScope(self, name):
        self.scope.append(name)
        self.symbolTable[name] = collections.OrderedDict()


    def addSymbol(self, id, typ, val=None):
        scope = self.scope[-1]
        if not scope in self.symbolTable:
            self.symbolTable[scope] = collections.OrderedDict()
        if not id in self.symbolTable[scope]:
            self.symbolTable[scope][id] = {'value':val,'type':typ}
        else:
            if not self.error:
                self.error = id
        
