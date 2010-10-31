actions = { 'GET'       : 0x00000001,
            'HEAD'      : 0x00000002,
            'PUT'       : 0x00000004,
            'OPTIONS'   : 0x00000008,
            'PROPFIND'  : 0x00000010,
            'PROPPATCH' : 0x00000020, 
            'MKCOL'     : 0x00000040,
            'REPORT'    : 0x00000080,
            'TRACE'     : 0x00000100,
            'POST'      : 0x00000200,
            'COPY'      : 0x00000400,
            'MOVE'      : 0x00000800,
            'DELETE'    : 0x00001000,
            'USERINFO'  : 0x00002000,
            'LOCK'      : 0x00004000,
            'UNLOCK'    : 0x00008000,
            'ADMIN'     : 0x00010000,
            'ALL'       : 0xFFFFFFFF
        }

user_root_acts = actions['GET'] | actions['PROPFIND'] | actions['MKCOL'] | actions['USERINFO'] | actions['OPTIONS'] 
user_dir_acts = actions['GET'] | actions['PROPFIND'] | actions['MKCOL'] | actions['USERINFO'] | actions['OPTIONS'] | actions['PUT'] | actions['LOCK'] | actions['UNLOCK'] | actions['COPY'] | actions['MOVE'] | actions['HEAD']