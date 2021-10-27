# compdist-servidor-negocios

Neste repositório encontra-se o código para os servidores de negócio do projeto "Banco de Dados com Webservices", para a disciplina de Computação Distribuída.

## Endpoints

## `GET /saldo/<conta_id>`

Retorna o saldo para a conta com ID `<conta_id>` passado na URL.

### Request Headers:

````
Authorization: <auth_token>
````

### Responses:

<table>
<tr>
<th> Status Code </th><th> Descrição </th>
</tr>

<tr></tr>

<tr>
<td>200</td>
<td>

Operação bem-sucedida.
```json   
{
    "conta": 123,
    "saldo": 1000
}
```

</td>
</tr>
    
<tr></tr>

<tr>
<td>401</td>
<td>

Ocorre quando o token de autenticação informado no header `Authorization` é invalido ou inexistente.
```json
{
    "message": "Não autorizado"
}
```

</td>
</tr>
    
<tr></tr>
    
<tr>
<td>500</td>
<td>

Ocorre caso haja algum erro no serviço que não seja erro de autenticação, tal como erro de lock de conta.
```json
{
    "message": "Não foi possível realizar a operação"
}
```

</td>
</tr>
</table>


## `PUT /deposito/<conta_id>/<valor>`

Realiza a transação de depósito de valor `<valor>` para a conta com ID `<conta_id>`.

### Request Headers:

```
Authorization: <auth_token>
```

### Responses:

<table>
<tr>
<th> Status Code </th><th> Descrição </th>
</tr>

<tr></tr>

<tr>
<td>200</td>
<td>

Operação bem-sucedida.
```json   
{
    "conta": 123,
    "saldo": 1000
}
```

</td>
</tr>
    
<tr></tr>

<tr>
<td>401</td>
<td>

Ocorre quando o token de autenticação informado no header `Authorization` é invalido ou inexistente.
```json
{
    "message": "Não autorizado"
}
```

</td>
</tr>
    
<tr></tr>
    
<tr>
<td>500</td>
<td>

Ocorre caso haja algum erro no serviço que não seja erro de autenticação, tal como erro de lock de conta.
```json
{
    "message": "Não foi possível realizar a operação"
}
```

</td>
</tr>
</table>

## `PUT /saque/<conta_id>/<valor>`

Realiza a transação de saque de valor `<valor>` na conta com ID `<conta_id>`.

<table>
<tr>
<th> Status Code </th><th> Descrição </th>
</tr>

<tr></tr>

<tr>
<td>200</td>
<td>

Operação bem-sucedida.
```json   
{
    "conta": 123,
    "saldo": 1000
}
```

</td>
</tr>
    
<tr></tr>

<tr>
<td>401</td>
<td>

Ocorre quando o token de autenticação informado no header `Authorization` é invalido ou inexistente.
```json
{
    "message": "Não autorizado"
}
```

</td>
</tr>
    
<tr></tr>
    
<tr>
<td>500</td>
<td>

Ocorre caso haja algum erro no serviço que não seja erro de autenticação, tal como erro de lock de conta.
```json
{
    "message": "Não foi possível realizar a operação"
}
```

</td>
</tr>
</table>

## `PUT /transferencia/<conta_origem>/<conta_dest>/<valor>`

Realiza uma transferência no valor `<valor>` da conta origem de ID `<conta_origem>` para a conta destino de ID `<conta_dest>`.

<table>
<tr>
<th> Status Code </th><th> Descrição </th>
</tr>

<tr></tr>

<tr>
<td>200</td>
<td>

Operação bem-sucedida.
```json   
{
    "conta": 123,
    "saldo": 1000
}
```

</td>
</tr>
    
<tr></tr>

<tr>
<td>401</td>
<td>

Ocorre quando o token de autenticação informado no header `Authorization` é invalido ou inexistente.
```json
{
    "message": "Não autorizado"
}
```

</td>
</tr>
    
<tr></tr>
    
<tr>
<td>500</td>
<td>

Ocorre caso haja algum erro no serviço que não seja erro de autenticação, tal como erro de lock de conta.
```json
{
    "message": "Não foi possível realizar a operação"
}
```

</td>
</tr>
</table>
