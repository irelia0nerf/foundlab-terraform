import React, { useState } from 'react';

function TransactionModal({ isOpen, onClose }) {
  const [status, setStatus] = useState('');
  const [txHash, setTxHash] = useState('');

  const handleSignTransaction = async () => {
    setStatus('Aguardando assinatura na carteira...');
    if (typeof window.ethereum === 'undefined') {
      setStatus('Erro: MetaMask ou outra carteira Web3 não encontrada.');
      return;
    }

    try {
      const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
      const txParams = {
        from: accounts[0],
        to: '0x0000000000000000000000000000000000000000', // Endereço de exemplo
        value: '0x0' 
      };

      const signedTxHash = await window.ethereum.request({
        method: 'eth_sendTransaction',
        params: [txParams],
      });
      
      setTxHash(signedTxHash);
      setStatus('Transação assinada e enviada com sucesso!');
      console.log('Hash da Transação Assinada:', signedTxHash);

    } catch (error) {
      console.error('Erro ao assinar transação:', error);
      setStatus(`Erro: ${error.message}`);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <h3>Interação Não-Custodial</h3>
        <p>Esta ação requer uma assinatura da sua carteira Web3. A FoundLab nunca terá acesso às suas chaves privadas.</p>
        <button onClick={handleSignTransaction}>Assinar Transação</button>
        <button onClick={onClose}>Fechar</button>
        {status && <p><strong>Status:</strong> {status}</p>}
        {txHash && <p><strong>Tx Hash:</strong> {txHash}</p>}
      </div>
    </div>
  );
}

export default TransactionModal;